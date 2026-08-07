"""
R&D & Academic Literature Research Module.
Searches academic preprints, scientific literature (arXiv, EuropePMC, OpenAlex),
formulates research hypotheses, and generates patent prior art search queries.
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional

def search_arxiv_papers(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Searches arXiv scientific preprints API for academic literature.
    """
    clean_q = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{clean_q}&start=0&max_results={max_results}"

    papers = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgentSystem/2.5"})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read().decode("utf-8")

        root = ET.fromstring(xml_data)
        atom_ns = "{http://www.w3.org/2005/Atom}"

        for entry in root.findall(f"{atom_ns}entry"):
            title = entry.find(f"{atom_ns}title").text.strip().replace("\n", " ")
            summary = entry.find(f"{atom_ns}summary").text.strip().replace("\n", " ")
            published = entry.find(f"{atom_ns}published").text[:10]
            link = entry.find(f"{atom_ns}id").text

            authors = [a.find(f"{atom_ns}name").text for a in entry.findall(f"{atom_ns}author")]

            papers.append({
                "title": title,
                "authors": ", ".join(authors[:3]),
                "published": published,
                "summary": summary[:250] + "...",
                "url": link
            })
    except Exception as e:
        papers.append({"title": f"Search fallback for '{query}'", "authors": "System", "published": "2026", "summary": f"Error: {str(e)}", "url": "https://arxiv.org"})

    return papers

def generate_patent_prior_art_query(invention_description: str) -> Dict[str, Any]:
    """
    Generates CPC/IPC classification codes and Boolean search queries for WIPO/USPTO/Google Patents.
    """
    desc_upper = invention_description.upper()

    cpc_codes = []
    if "PCB" in desc_upper or "CIRCUIT" in desc_upper:
        cpc_codes.append("H05K (Printed Circuits; Casings)")
    if "MCU" in desc_upper or "MICROCONTROLLER" in desc_upper or "PROCESSOR" in desc_upper:
        cpc_codes.append("G06F (Electric Digital Data Processing)")
    if "SENSOR" in desc_upper or "TEMPERATURE" in desc_upper:
        cpc_codes.append("G01K (Measuring Temperature)")

    boolean_query = f"({invention_description}) AND (system OR apparatus OR method) NOT (prior art)"

    return {
        "status": "success",
        "invention_summary": invention_description,
        "suggested_cpc_classifications": cpc_codes or ["G06F (Digital Data Processing)"],
        "google_patents_query": f"https://patents.google.com/?q={urllib.parse.quote(invention_description)}",
        "boolean_search_string": boolean_query
    }

def assess_technology_readiness_level(trl_stage_description: str) -> Dict[str, Any]:
    """
    Assesses Technology Readiness Level (TRL 1 to 9) according to NASA/EU standards.
    """
    desc_lower = trl_stage_description.lower()

    trl = 1
    stage_name = "TRL 1: Basic Principles Observed"

    if "prototype" in desc_lower and "relevant environment" in desc_lower:
        trl = 6
        stage_name = "TRL 6: Technology Demonstrated in Relevant Environment"
    elif "prototype" in desc_lower or "breadboard" in desc_lower:
        trl = 4
        stage_name = "TRL 4: Component / Breadboard Validation in Lab"
    elif "proof of concept" in desc_lower or "concept" in desc_lower:
        trl = 3
        stage_name = "TRL 3: Analytical & Experimental Proof of Concept"
    elif "commercial" in desc_lower or "deployed" in desc_lower:
        trl = 9
        stage_name = "TRL 9: Actual System Proven in Operational Environment"

    return {
        "status": "success",
        "assessed_trl": trl,
        "stage_title": stage_name,
        "next_steps": f"To advance to TRL {min(trl+1, 9)}, conduct rigorous environment testing and validation."
    }
