"""
ESD Protection & TVS Diode Selection Engine.
Selects TVS diodes and ESD protection networks for USB, Ethernet, CAN, and GPIO lines
compliant with IEC 61000-4-2 (Level 4, 8kV contact / 15kV air discharge).
"""

from typing import Dict, Any

def design_esd_protection(
    interface_type: str = "USB2.0",
    working_voltage_v: float = 3.3,
    data_rate_mbps: float = 480.0
) -> Dict[str, Any]:
    """
    Selects TVS diodes and ESD protection networks based on interface specs.
    """
    if data_rate_mbps > 100.0 or "USB" in interface_type.upper():
        max_cap_pf = 0.5
        rec_part = "USBLC6-2SC6 / SP0503BAHTG"
        clamping_v = 9.0
    elif "CAN" in interface_type.upper() or "RS485" in interface_type.upper():
        max_cap_pf = 30.0
        rec_part = "PESD2CAN / NVTFS5C460NL"
        clamping_v = 40.0
    else:  # General GPIO / Low speed
        max_cap_pf = 15.0
        rec_part = "ESD5Z3.3T1G / PRTR5V0U2X"
        clamping_v = 6.5

    return {
        "status": "success",
        "interface_type": interface_type,
        "working_voltage_v": working_voltage_v,
        "data_rate_mbps": data_rate_mbps,
        "iec_standard": "IEC 61000-4-2 Level 4 (8kV Contact / 15kV Air)",
        "max_parasitic_capacitance_pf": max_cap_pf,
        "max_clamping_voltage_v": clamping_v,
        "recommended_tvs_diode": rec_part,
        "layout_rule": "Place TVS diode immediately adjacent to connector pins before series resistors or IC pins."
    }
