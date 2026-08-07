"""
Multidisciplinary Project Workspace Architecture Generator.
Generates complete repository directory structure for multidisciplinary projects
combining Firmware, KiCad Schematics, OpenSCAD 3D Enclosure, Edge AI Model, and Docs.
"""

import os
from typing import Dict, Any, List

def create_multidisciplinary_project(project_name: str, base_dir: str = ".") -> Dict[str, Any]:
    """
    Creates a unified multidisciplinary engineering repository structure:
    project_name/
      ├── firmware/       (C/C++ platformio/STM32 CMake)
      ├── hardware/       (KiCad schematic + PCB BOM)
      ├── mechanical/     (OpenSCAD 3D enclosure + STL)
      ├── edge_ai/        (TFLite Micro / ESP-DL model wrappers)
      └── docs/           (Datasheets & Architecture specification)
    """
    target_root = os.path.join(base_dir, project_name)

    directories = [
        "firmware/src",
        "firmware/include",
        "hardware/schematics",
        "hardware/gerber",
        "mechanical/cad",
        "mechanical/stl",
        "edge_ai/models",
        "edge_ai/include",
        "docs/datasheets"
    ]

    created_dirs = []
    for d in directories:
        dir_path = os.path.join(target_root, d)
        os.makedirs(dir_path, exist_ok=True)
        created_dirs.append(dir_path)

    # 1. Main Firmware main.cpp
    main_cpp = os.path.join(target_root, "firmware/src/main.cpp")
    if not os.path.exists(main_cpp):
        with open(main_cpp, "w") as f:
            f.write(f'''// Multidisciplinary Firmware Entrypoint for {project_name}
#include <Arduino.h>
#include <Wire.h>

void setup() {{
    Serial.begin(115200);
    Wire.begin(21, 22); // I2C SDA=GPIO21, SCL=GPIO22
    Serial.println("🤖 {project_name} Multidisciplinary System Initialized!");
}}

void loop() {{
    delay(1000);
}}
''')

    # 2. OpenSCAD 3D Enclosure Template
    scad_file = os.path.join(target_root, "mechanical/cad/enclosure.scad")
    if not os.path.exists(scad_file):
        with open(scad_file, "w") as f:
            f.write(f'// OpenSCAD 3D Enclosure Template for {project_name}\ncube([60, 40, 20]);\n')

    # 3. Project Architecture README.md
    readme_file = os.path.join(target_root, "README.md")
    if not os.path.exists(readme_file):
        with open(readme_file, "w") as f:
            f.write(f'''# 🚀 {project_name} — Multidisciplinary Engineering Project

Auto-generated workspace structure for **Firmware + Hardware + Mechanical CAD + Edge AI**.

## 📁 Repository Structure
- `firmware/`: ESP32 / STM32 C++ C code & PlatformIO build config.
- `hardware/`: KiCad S-expression schematic & PCB BOM CSV.
- `mechanical/`: OpenSCAD 3D parametric enclosure script & STL files.
- `edge_ai/`: TFLite Micro / ESP-DL INT8 quantized neural network models.
- `docs/`: PDF datasheets & system architecture documentation.
''')

    return {
        "status": "success",
        "project_name": project_name,
        "root_directory": target_root,
        "directories_created": len(created_dirs),
        "structure": directories
    }
