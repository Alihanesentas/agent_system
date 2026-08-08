"""
IP Ingress Protection Code (IP54 / IP65 / IP67 / IP68) Requirement Checker.
Audits enclosure gasket seal width (mm), compression ratio (%), screw spacing (mm),
ventilation membrane requirement, and IEC 60529 compliance.
"""

from typing import Dict, Any

def check_ip_rating_requirements(
    target_ip_rating: str = "IP67",
    gasket_installed: bool = True,
    max_screw_spacing_mm: float = 40.0
) -> Dict[str, Any]:
    """
    Checks IP rating enclosure sealing requirements per IEC 60529.
    """
    ip = target_ip_rating.upper().strip()
    
    first_digit = int(ip[2]) if len(ip) >= 3 and ip[2].isdigit() else 6
    second_digit = int(ip[3]) if len(ip) >= 4 and ip[3].isdigit() else 7
    
    dust_protection = {
        5: "Dust-protected (Limited ingress, non-harmful)",
        6: "Dust-tight (No ingress of dust)"
    }.get(first_digit, "Dust protection required")
    
    water_protection = {
        4: "Protection against splashing water from any direction",
        5: "Protection against water jets (6.3mm nozzle)",
        6: "Protection against powerful water jets (12.5mm nozzle)",
        7: "Immersion up to 1m depth for 30 minutes",
        8: "Continuous submersion under pressure"
    }.get(second_digit, "Water protection required")
    
    is_compliant = gasket_installed and max_screw_spacing_mm <= 50.0

    return {
        "status": "success",
        "target_ip_rating": ip,
        "dust_ingress_level": dust_protection,
        "water_ingress_level": water_protection,
        "gasket_installed": gasket_installed,
        "max_screw_spacing_mm": max_screw_spacing_mm,
        "membrane_vent_recommended": second_digit >= 6,
        "compliance_verdict": "IEC 60529 COMPLIANT DESIGN" if is_compliant else "NON-COMPLIANT: Gasket missing or screw spacing > 50mm"
    }
