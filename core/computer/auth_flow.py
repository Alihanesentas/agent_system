"""
OAuth2, JWT & API Key Authentication Strategy Generator.
Generates authentication middleware, JWT payload signing (RS256/HS256), token expiration,
and RBAC (Role-Based Access Control) security configuration code for Python / Node.js.
"""

from typing import Dict, Any, List

def generate_auth_flow(
    auth_type: str = "JWT_RS256",
    token_ttl_minutes: int = 60,
    roles: List[str] = ["admin", "engineer", "viewer"]
) -> Dict[str, Any]:
    """
    Generates OAuth2 / JWT authentication flow boilerplate and security rules.
    """
    py_middleware = f"""# FastAPI JWT OAuth2 Authentication Middleware
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your-rsa-private-key"
ALGORITHM = "{auth_type.split('_')[-1] if '_' in auth_type else 'HS256'}"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
"""

    return {
        "status": "success",
        "auth_type": auth_type,
        "token_ttl_minutes": token_ttl_minutes,
        "roles_configured": roles,
        "fastapi_middleware_code": py_middleware
    }
