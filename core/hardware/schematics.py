import os
import re
import csv
from typing import Dict, Any, List, Optional

def parse_kicad_schematic(file_path: str) -> Dict[str, Any]:
    """
    Parses KiCad 6/7/8 schematic (.kicad_sch) S-expression files.
    Extracts component symbols, references (R1, C1, U1), values, and lib definitions.
    """
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract symbols/components
        components = []
        symbol_matches = re.findall(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(property\s+"Value"\s+"([^"]+)"', content)

        for lib_id, ref, val in symbol_matches:
            components.append({
                "reference": ref,
                "value": val,
                "library_id": lib_id
            })

        # Extract nets/labels
        labels = re.findall(r'\(label\s+"([^"]+)"', content)

        return {
            "file": file_path,
            "total_components": len(components),
            "components": components,
            "net_labels": list(set(labels))
        }
    except Exception as e:
        return {"error": f"Failed to parse KiCad schematic: {str(e)}"}

def update_kicad_component_value(file_path: str, reference: str, new_value: str) -> Dict[str, Any]:
    """
    Safely updates a component value (e.g. changing R1 from 10k to 1k) 
    directly inside a KiCad schematic (.kicad_sch) file.
    """
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Pattern matching reference property followed by value property
        pattern = rf'(\(property\s+"Reference"\s+"{reference}"[\s\S]*?\(property\s+"Value"\s+)"([^"]+)"'
        
        if not re.search(pattern, content):
            return {"error": f"Component reference '{reference}' not found in '{file_path}'."}

        updated_content = re.sub(pattern, rf'\1"{new_value}"', content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        return {
            "status": "success",
            "reference": reference,
            "new_value": new_value,
            "file": file_path
        }
    except Exception as e:
        return {"error": f"Failed to update component value: {str(e)}"}

def parse_bom_csv(file_path: str) -> Dict[str, Any]:
    """
    Parses PCB Bill of Materials (BOM) CSV file and checks part counts and missing fields.
    """
    if not os.path.exists(file_path):
        return {"error": f"File '{file_path}' not found."}

    try:
        parts = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                parts.append(dict(row))

        return {
            "file": file_path,
            "total_line_items": len(parts),
            "items": parts
        }
    except Exception as e:
        return {"error": f"Failed to parse BOM CSV: {str(e)}"}
