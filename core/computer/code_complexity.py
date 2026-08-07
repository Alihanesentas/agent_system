"""
Cyclomatic Code Complexity & Maintainability Index Auditor Engine.
Analyzes AST branch conditions (if/for/while/switch) and rates code maintainability.
"""

import ast
from typing import Dict, Any

def audit_code_complexity(python_code: str) -> Dict[str, Any]:
    """Calculates cyclomatic complexity score and maintainability grade."""
    try:
        tree = ast.parse(python_code)
        branch_count = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                branch_count += 1
        
        grade = "A (Clean & Maintainable)" if branch_count <= 5 else ("B (Moderate)" if branch_count <= 10 else "C (High Complexity)")
        return {
            "status": "success",
            "cyclomatic_complexity": branch_count,
            "maintainability_grade": grade
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
