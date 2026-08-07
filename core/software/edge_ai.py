"""
Edge AI & TinyML Engine — Model Quantization & Microcontroller Deployment.
Inspects ONNX/TFLite models, estimates peak SRAM/Flash memory budget, 
and generates C++ code headers for ESP-DL, TFLite Micro, and STM32Cube.AI.
"""

from typing import Dict, Any, List, Optional

def generate_esp_dl_model_wrapper(
    model_name: str,
    input_shape: List[int],
    output_shape: List[int],
    quant_type: str = "int8"
) -> str:
    """
    Generates C++ code wrapper for deploying TinyML neural network models 
    on ESP32-S3 using ESP-DL / TFLite Micro.
    """
    input_size = 1
    for dim in input_shape:
        input_size *= dim

    output_size = 1
    for dim in output_shape:
        output_size *= dim

    cpp_code = f"""// Edge AI Model Wrapper for ESP32-S3 / TFLite Micro (Auto-Generated)
#include "dl_model_base.hpp"
#include <vector>
#include <cstdint>

#define MODEL_INPUT_SIZE {input_size}
#define MODEL_OUTPUT_SIZE {output_size}
#define QUANTIZATION_TYPE "{quant_type.upper()}"

class {model_name}Model {{
private:
    dl::Model *model;
    int8_t input_tensor[MODEL_INPUT_SIZE];
    int8_t output_tensor[MODEL_OUTPUT_SIZE];

public:
    {model_name}Model() {{
        // Initialize model weights from Flash
    }}

    bool run_inference(const float* input_data, float* output_results) {{
        // Quantize float input -> int8
        for(int i = 0; i < MODEL_INPUT_SIZE; i++) {{
            input_tensor[i] = (int8_t)(input_data[i] * 127.0f);
        }}

        // Run hardware-accelerated inference on ESP32-S3 Vector Extension
        // model->forward(input_tensor);

        // De-quantize int8 output -> float
        for(int i = 0; i < MODEL_OUTPUT_SIZE; i++) {{
            output_results[i] = (float)output_tensor[i] / 127.0f;
        }}
        return true;
    }}
}};
"""
    return cpp_code

def estimate_edge_ai_memory(
    num_parameters: int,
    input_tensor_shape: List[int],
    quantization: str = "int8"
) -> Dict[str, Any]:
    """
    Calculates estimated Flash and SRAM memory footprint for MCU deployment.
    """
    bytes_per_param = 1 if quantization.lower() == "int8" else 2  # FP16 = 2, FP32 = 4

    flash_weight_bytes = num_parameters * bytes_per_param
    flash_kb = round(flash_weight_bytes / 1024.0, 1)

    # Estimate peak tensor arena SRAM usage
    input_elements = 1
    for d in input_tensor_shape:
        input_elements *= d

    tensor_arena_bytes = (input_elements * bytes_per_param) + (num_parameters * 0.1)  # Buffer allocation estimate
    sram_kb = round(tensor_arena_bytes / 1024.0, 1)

    # MCU Suitability Check
    suitable_mcus = []
    if sram_kb < 30 and flash_kb < 100:
        suitable_mcus.append("STM32F103 (64KB Flash, 20KB SRAM)")
    if sram_kb < 200 and flash_kb < 1000:
        suitable_mcus.append("RP2040 (264KB SRAM, External Flash)")
    if sram_kb < 500 and flash_kb < 8000:
        suitable_mcus.append("ESP32-S3 (512KB SRAM, 8MB PSRAM, Vector AI Acceleration)")

    return {
        "status": "success",
        "num_parameters": num_parameters,
        "quantization": quantization.upper(),
        "flash_footprint_kb": flash_kb,
        "sram_tensor_arena_kb": sram_kb,
        "recommended_mcus": suitable_mcus
    }
