"""
RAG (Retrieval-Augmented Generation) Engine for Multi-Agent System.
Indexes project documents, datasheets (PDF/TXT/MD/Code), and retrieves
relevant context chunks to inject into LLM prompts for grounded answers.
"""

import os
import hashlib
from typing import List, Dict, Any, Optional

# ChromaDB lazy import (fails gracefully if not installed)
_chroma_client = None
_collection = None

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "rag_store")
COLLECTION_NAME = "agent_documents"

# ------------------------------------------------------------------
# Chunking Strategy
# ------------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    source: str = "unknown"
) -> List[Dict[str, Any]]:
    """
    Splits text into overlapping chunks optimized for retrieval.
    Each chunk carries metadata (source file, chunk index, char offsets).
    """
    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at paragraph or sentence boundary
        if end < len(text):
            # Prefer paragraph break
            para_break = text.rfind("\n\n", start, end)
            if para_break > start + chunk_size // 2:
                end = para_break + 2
            else:
                # Prefer sentence break
                sent_break = text.rfind(". ", start, end)
                if sent_break > start + chunk_size // 2:
                    end = sent_break + 2

        chunk_text_str = text[start:end].strip()
        if chunk_text_str:
            chunks.append({
                "text": chunk_text_str,
                "metadata": {
                    "source": source,
                    "chunk_index": idx,
                    "char_start": start,
                    "char_end": end
                }
            })
            idx += 1

        start = end - chunk_overlap
        if start >= len(text):
            break

    return chunks

# ------------------------------------------------------------------
# ChromaDB Vector Store Management
# ------------------------------------------------------------------

def _get_collection():
    """Lazily initializes ChromaDB persistent client and collection."""
    global _chroma_client, _collection
    if _collection is not None:
        return _collection

    try:
        import chromadb
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        return _collection
    except ImportError:
        print("⚠️  chromadb is not installed. Run: pip install chromadb")
        return None
    except Exception as e:
        print(f"⚠️  ChromaDB initialization error: {e}")
        return None

def _content_hash(text: str) -> str:
    """Returns a short SHA-256 hash for deduplication."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

# ------------------------------------------------------------------
# Indexing (Add Documents)
# ------------------------------------------------------------------

def index_file(file_path: str) -> Dict[str, Any]:
    """
    Reads a single file, chunks it, and indexes into ChromaDB.
    Supports: .txt, .md, .py, .c, .h, .cpp, .json, .csv, .kicad_sch, .pdf
    """
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    ext = os.path.splitext(file_path)[1].lower()

    # PDF extraction
    if ext == ".pdf":
        text = _extract_pdf_text(file_path)
        if text.startswith("Error"):
            return {"error": text}
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            return {"error": f"Cannot read file: {e}"}

    if not text.strip():
        return {"error": f"File '{file_path}' is empty or unreadable."}

    chunks = chunk_text(text, source=os.path.basename(file_path))
    collection = _get_collection()
    if collection is None:
        return {"error": "ChromaDB not available."}

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        doc_id = f"{os.path.basename(file_path)}_{_content_hash(chunk['text'])}"
        ids.append(doc_id)
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])

    # Upsert to avoid duplicates
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    return {
        "status": "success",
        "file": file_path,
        "chunks_indexed": len(chunks),
        "total_chars": len(text)
    }

def index_directory(dir_path: str, extensions: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Recursively indexes all matching files in a directory.
    Default extensions: .txt, .md, .py, .c, .h, .cpp, .json, .csv, .kicad_sch, .pdf
    """
    if extensions is None:
        extensions = [".txt", ".md", ".py", ".c", ".h", ".cpp", ".json", ".csv", ".kicad_sch", ".pdf"]

    results = []
    total_chunks = 0

    for root, dirs, files in os.walk(dir_path):
        # Skip hidden dirs and common non-project dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "__pycache__", ".venv", "rag_store"]]
        for fname in files:
            if any(fname.endswith(ext) for ext in extensions):
                fpath = os.path.join(root, fname)
                res = index_file(fpath)
                if res.get("status") == "success":
                    total_chunks += res["chunks_indexed"]
                results.append(res)

    return {
        "status": "success",
        "files_processed": len(results),
        "total_chunks_indexed": total_chunks,
        "details": results
    }

# ------------------------------------------------------------------
# Retrieval (Search)
# ------------------------------------------------------------------

def search(query: str, n_results: int = 5, source_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Semantic search across indexed documents.
    Returns top-N most relevant chunks with similarity scores.
    """
    collection = _get_collection()
    if collection is None:
        return [{"error": "ChromaDB not available."}]

    where_filter = None
    if source_filter:
        where_filter = {"source": source_filter}

    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]

    hits = []
    if results and results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            distance = results["distances"][0][i] if results["distances"] else 0.0
            similarity = round(1.0 - distance, 4)  # cosine distance → similarity
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            hits.append({
                "text": doc,
                "similarity": similarity,
                "source": meta.get("source", "unknown"),
                "chunk_index": meta.get("chunk_index", -1)
            })

    return hits

def build_rag_context(query: str, n_results: int = 3, max_context_chars: int = 3000) -> str:
    """
    Builds a formatted context string from RAG retrieval results,
    ready to be prepended to an LLM prompt.
    """
    hits = search(query, n_results=n_results)

    if not hits or "error" in hits[0]:
        return ""

    context_parts = []
    total_chars = 0

    for hit in hits:
        if total_chars + len(hit["text"]) > max_context_chars:
            break
        context_parts.append(
            f"[Source: {hit['source']} | Relevance: {hit['similarity']:.0%}]\n{hit['text']}"
        )
        total_chars += len(hit["text"])

    if not context_parts:
        return ""

    return (
        "=== RETRIEVED CONTEXT (RAG) ===\n"
        + "\n---\n".join(context_parts)
        + "\n=== END CONTEXT ===\n\n"
    )

def get_index_stats() -> Dict[str, Any]:
    """Returns statistics about the current RAG index."""
    collection = _get_collection()
    if collection is None:
        return {"error": "ChromaDB not available."}

    count = collection.count()
    return {
        "total_chunks": count,
        "collection_name": COLLECTION_NAME,
        "persist_directory": CHROMA_PERSIST_DIR
    }

# ------------------------------------------------------------------
# PDF Text Extraction Helper
# ------------------------------------------------------------------

def _extract_pdf_text(file_path: str) -> str:
    """Extracts text from PDF files using pdfplumber (tables + paragraphs)."""
    try:
        import pdfplumber
        full_text = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract tables first
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            if row:
                                cleaned = [str(cell).strip() if cell else "" for cell in row]
                                full_text.append(" | ".join(cleaned))

                # Extract remaining text
                text = page.extract_text()
                if text:
                    full_text.append(f"\n--- Page {page_num} ---\n{text}")

        return "\n".join(full_text)
    except ImportError:
        return "Error: pdfplumber is not installed. Run: pip install pdfplumber"
    except Exception as e:
        return f"Error extracting PDF: {e}"
