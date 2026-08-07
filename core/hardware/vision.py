import os
import base64
from typing import Dict, Any, Optional

def encode_image_to_base64(image_path: str) -> Dict[str, Any]:
    """
    Encodes an image file (PNG, JPG, BMP, WEBP) to Base64 format 
    ready for Multimodal Vision LLM input payload.
    """
    if not os.path.exists(image_path):
        return {"error": f"Image file '{image_path}' not found."}

    ext = os.path.splitext(image_path)[1].lower().strip(".")
    mime_type = f"image/{ext}" if ext in ["png", "jpg", "jpeg", "webp", "gif"] else "image/png"

    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        
        return {
            "status": "success",
            "file": image_path,
            "mime_type": mime_type,
            "data_url": f"data:{mime_type};base64,{encoded_string}",
            "base64_length": len(encoded_string)
        }
    except Exception as e:
        return {"error": f"Failed to encode image: {str(e)}"}
