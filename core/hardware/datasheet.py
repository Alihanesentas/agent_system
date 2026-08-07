"""
Datasheet PDF Extractor — Advanced PDF Parser for Electronic Component Datasheets.
Extracts pin tables, electrical characteristics, absolute maximum ratings,
section headers, and key specifications from component datasheets.
"""

import os
import re
from typing import Dict, Any, List, Optional

def extract_datasheet(file_path: str) -> Dict[str, Any]:
    """
    Comprehensive datasheet extraction pipeline.
    Extracts: sections, pin tables, electrical specs, absolute max ratings, and key parameters.
    """
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    try:
        import pdfplumber
    except ImportError:
        return {"error": "pdfplumber not installed. Run: pip install pdfplumber"}

    result = {
        "file": file_path,
        "total_pages": 0,
        "sections": [],
        "pin_tables": [],
        "electrical_specs": [],
        "absolute_max_ratings": [],
        "key_parameters": {},
        "all_tables": [],
        "full_text_preview": ""
    }

    try:
        with pdfplumber.open(file_path) as pdf:
            result["total_pages"] = len(pdf.pages)
            full_text_parts = []

            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                full_text_parts.append(text)

                # Extract all tables from this page
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        cleaned_table = _clean_table(table)
                        table_data = {
                            "page": page_num,
                            "rows": len(cleaned_table),
                            "columns": len(cleaned_table[0]) if cleaned_table else 0,
                            "header": cleaned_table[0] if cleaned_table else [],
                            "data": cleaned_table[1:] if len(cleaned_table) > 1 else []
                        }

                        # Classify table type
                        table_type = _classify_table(cleaned_table)
                        table_data["type"] = table_type

                        if table_type == "pin_table":
                            result["pin_tables"].append(table_data)
                        elif table_type == "electrical_spec":
                            result["electrical_specs"].append(table_data)
                        elif table_type == "absolute_max":
                            result["absolute_max_ratings"].append(table_data)

                        result["all_tables"].append(table_data)

            full_text = "\n".join(full_text_parts)

            # Extract section headers
            result["sections"] = _extract_sections(full_text)

            # Extract key parameters from text
            result["key_parameters"] = _extract_key_parameters(full_text)

            # Preview first 2000 chars
            result["full_text_preview"] = full_text[:2000]

    except Exception as e:
        result["error"] = f"PDF extraction failed: {str(e)}"

    return result

def extract_pin_table(file_path: str) -> List[Dict[str, str]]:
    """Extracts only pin configuration tables from a datasheet PDF."""
    data = extract_datasheet(file_path)
    pins = []

    for table in data.get("pin_tables", []):
        header = [str(h).lower().strip() for h in table.get("header", [])]
        for row in table.get("data", []):
            pin = {}
            for i, cell in enumerate(row):
                if i < len(header):
                    pin[header[i]] = str(cell).strip() if cell else ""
            if pin:
                pins.append(pin)

    return pins

def extract_electrical_specs(file_path: str) -> List[Dict[str, str]]:
    """Extracts electrical characteristics tables from a datasheet PDF."""
    data = extract_datasheet(file_path)
    specs = []

    for table in data.get("electrical_specs", []):
        header = [str(h).lower().strip() for h in table.get("header", [])]
        for row in table.get("data", []):
            spec = {}
            for i, cell in enumerate(row):
                if i < len(header):
                    spec[header[i]] = str(cell).strip() if cell else ""
            if spec:
                specs.append(spec)

    return specs

def summarize_datasheet(file_path: str) -> str:
    """
    Generates a concise text summary of a datasheet suitable 
    for LLM context injection or agent briefing.
    """
    data = extract_datasheet(file_path)

    if "error" in data:
        return f"Error: {data['error']}"

    lines = [f"=== DATASHEET SUMMARY: {os.path.basename(file_path)} ({data['total_pages']} pages) ==="]

    # Key parameters
    params = data.get("key_parameters", {})
    if params:
        lines.append("\n📋 Key Parameters:")
        for k, v in params.items():
            lines.append(f"  • {k}: {v}")

    # Sections
    sections = data.get("sections", [])
    if sections:
        lines.append(f"\n📑 Sections Found ({len(sections)}):")
        for s in sections[:15]:
            lines.append(f"  • {s}")

    # Pin tables
    pin_tables = data.get("pin_tables", [])
    if pin_tables:
        total_pins = sum(t.get("rows", 0) - 1 for t in pin_tables)
        lines.append(f"\n📌 Pin Tables: {len(pin_tables)} table(s), ~{total_pins} pins")

    # Electrical specs
    elec = data.get("electrical_specs", [])
    if elec:
        lines.append(f"\n⚡ Electrical Characteristics: {len(elec)} table(s)")

    # Absolute max
    abs_max = data.get("absolute_max_ratings", [])
    if abs_max:
        lines.append(f"\n🔴 Absolute Maximum Ratings: {len(abs_max)} table(s)")

    # All tables
    lines.append(f"\n📊 Total Tables Extracted: {len(data.get('all_tables', []))}")

    return "\n".join(lines)

# ------------------------------------------------------------------
# Internal Helpers
# ------------------------------------------------------------------

def _clean_table(table: List) -> List[List[str]]:
    """Cleans a raw table: strips whitespace, replaces None with empty strings."""
    cleaned = []
    for row in table:
        if row:
            cleaned_row = [str(cell).strip() if cell else "" for cell in row]
            # Skip completely empty rows
            if any(c for c in cleaned_row):
                cleaned.append(cleaned_row)
    return cleaned

def _classify_table(table: List[List[str]]) -> str:
    """Classifies a table type based on header content."""
    if not table:
        return "unknown"

    header_text = " ".join(str(h).lower() for h in table[0])

    pin_keywords = ["pin", "gpio", "port", "function", "alternate", "af", "i/o", "name", "number"]
    elec_keywords = ["parameter", "condition", "min", "typ", "max", "unit", "symbol", "voltage", "current"]
    abs_max_keywords = ["absolute", "maximum", "rating", "stress", "damage"]

    if any(kw in header_text for kw in pin_keywords):
        return "pin_table"
    elif any(kw in header_text for kw in abs_max_keywords):
        return "absolute_max"
    elif any(kw in header_text for kw in elec_keywords):
        return "electrical_spec"
    else:
        return "general"

def _extract_sections(text: str) -> List[str]:
    """Extracts section headers from datasheet text."""
    # Match numbered sections and capitalized headers
    patterns = [
        r'^(\d+\.?\d*\.?\d*\s+[A-Z][A-Za-z\s/&\-]+)',  # "1.2 Pin Configuration"
        r'^([A-Z][A-Z\s/&\-]{3,})$',                      # "ELECTRICAL CHARACTERISTICS"
    ]

    sections = []
    for line in text.split("\n"):
        line = line.strip()
        for pattern in patterns:
            match = re.match(pattern, line)
            if match and len(match.group(1)) < 80:
                sections.append(match.group(1).strip())
                break

    return list(dict.fromkeys(sections))  # Remove duplicates while preserving order

def _extract_key_parameters(text: str) -> Dict[str, str]:
    """Extracts key parameters (voltage, frequency, temperature) from datasheet text."""
    params = {}

    patterns = {
        "supply_voltage": r'(?:supply|operating)\s+voltage[:\s]*(\d+\.?\d*\s*(?:V|mV)(?:\s*(?:to|~|-)\s*\d+\.?\d*\s*(?:V|mV))?)',
        "max_frequency": r'(?:max(?:imum)?|clock)\s+frequency[:\s]*(\d+\.?\d*\s*(?:MHz|GHz|kHz))',
        "operating_temp": r'(?:operating|ambient)\s+temperature[:\s]*([-]?\d+\s*(?:°C|C)\s*(?:to|~|-)\s*[-]?\d+\s*(?:°C|C))',
        "flash_memory": r'(?:flash|program)\s+memory[:\s]*(\d+\.?\d*\s*(?:KB|MB|GB|kB|Kbytes|Mbytes))',
        "ram": r'(?:RAM|SRAM|data\s+memory)[:\s]*(\d+\.?\d*\s*(?:KB|MB|GB|kB|Kbytes|bytes))',
        "package": r'(?:package|pkg)[:\s]*(\w+[-]?\d+\w*)',
    }

    text_lower = text.lower()
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            params[key] = match.group(1).strip()

    return params
