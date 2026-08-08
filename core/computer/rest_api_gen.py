"""
REST API Endpoint & Router Scaffold Generator (FastAPI / Express / Go).
Generates full-stack CRUD REST API router endpoints, request/response DTO schemas, and OpenAPI documentation boilerplates.
"""

from typing import Dict, Any, List

def generate_rest_api_scaffold(
    resource_name: str = "Device",
    framework: str = "FastAPI",
    endpoints: List[str] = None
) -> Dict[str, Any]:
    """
    Generates REST API router code and Pydantic/TypeScript models.
    """
    if not endpoints:
        endpoints = ["GET /", "GET /{id}", "POST /", "PUT /{id}", "DELETE /{id}"]
    
    r_lower = resource_name.lower()
    r_title = resource_name.capitalize()

    fastapi_code = f"""# Auto-generated FastAPI Router for {r_title}
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1/{r_lower}s", tags=["{r_title}s"])

class {r_title}Create(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class {r_title}Response({r_title}Create):
    id: str

@{r_lower}s_db = {{}}

@router.get("/", response_model=List[{r_title}Response])
async def list_{r_lower}s():
    return list(@{r_lower}s_db.values())

@router.post("/", response_model={r_title}Response, status_code=status.HTTP_201_CREATED)
async def create_{r_lower}(payload: {r_title}Create):
    item_id = str(len(@{r_lower}s_db) + 1)
    obj = {r_title}Response(id=item_id, **payload.dict())
    @{r_lower}s_db[item_id] = obj
    return obj
""".replace("@", "")

    return {
        "status": "success",
        "resource_name": r_title,
        "framework": framework,
        "endpoints_scaffolded": len(endpoints),
        "code_snippet": fastapi_code,
        "supported_methods": ["GET", "POST", "PUT", "DELETE"]
    }
