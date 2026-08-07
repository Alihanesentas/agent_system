"""
Core Computer Science & Web Engineering Sub-Package Entrypoint.
Provides modular re-exports for:
- web_stack: Full-Stack FastAPI / Express REST APIs
- microservices: gRPC Protobuf & Event Bus
- frontend_gen: React Vite / Next.js TSX Components
- code_complexity: AST Cyclomatic Complexity Auditor
"""

from core.computer.web_stack import generate_web_api_architecture
from core.computer.microservices import generate_microservice_proto
from core.computer.frontend_gen import generate_react_component
from core.computer.code_complexity import audit_code_complexity
