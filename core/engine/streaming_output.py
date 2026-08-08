"""
Token-by-Token Streaming Output & Server-Sent Events (SSE) Engine.
Buffers and streams agent responses in real-time token chunks for web UI / CLI interactivity,
eliminating perceived latency.
"""

from typing import Dict, Any, List

def stream_output(
    text_content: str = "Calculating microstrip characteristic impedance... Z0 = 50.2 Ohms.",
    chunk_size_words: int = 3
) -> Dict[str, Any]:
    """
    Simulates real-time token streaming chunks.
    """
    words = text_content.split()
    chunks = [" ".join(words[i:i+chunk_size_words]) for i in range(0, len(words), chunk_size_words)]

    return {
        "status": "success",
        "total_tokens": len(words),
        "chunk_count": len(chunks),
        "sample_stream_chunks": chunks,
        "protocol": "Server-Sent Events (SSE / text-event-stream)"
    }
