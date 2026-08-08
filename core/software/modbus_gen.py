"""
Modbus RTU/TCP Register Map & C Struct Generator.
Generates industrial Modbus holding registers (4xxxx) and input registers (3xxxx)
maps and C/C++ struct definitions for industrial IoT controllers.
"""

from typing import Dict, Any, List

def generate_modbus_map(
    device_name: str = "IndustrialSensorNode",
    slave_address: int = 1
) -> Dict[str, Any]:
    """
    Generates Modbus register map and C header structs.
    """
    registers = [
        {"address": 40001, "name": "DeviceStatus", "type": "UINT16", "access": "RO", "unit": "bitmap"},
        {"address": 40002, "name": "Temperature_C_x10", "type": "INT16", "access": "RO", "unit": "0.1 degC"},
        {"address": 40003, "name": "Pressure_mbar", "type": "UINT16", "access": "RO", "unit": "mbar"},
        {"address": 40004, "name": "SetPointTemp", "type": "UINT16", "access": "RW", "unit": "0.1 degC"},
        {"address": 40005, "name": "ControlFlags", "type": "UINT16", "access": "RW", "unit": "flags"},
    ]

    c_struct = f"""// Auto-generated Modbus Map for {device_name} (Slave #{slave_address})
typedef struct __attribute__((packed)) {{
    uint16_t device_status;      // 40001 (RO)
    int16_t  temp_c_x10;         // 40002 (RO)
    uint16_t pressure_mbar;      // 40003 (RO)
    uint16_t setpoint_temp;      // 40004 (RW)
    uint16_t control_flags;      // 40005 (RW)
}} modbus_map_{device_name.lower()}_t;
"""

    return {
        "status": "success",
        "device_name": device_name,
        "slave_address": slave_address,
        "total_holding_registers": len(registers),
        "registers": registers,
        "c_struct_code": c_struct
    }
