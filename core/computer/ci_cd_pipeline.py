"""
CI/CD Pipeline YAML Generator (GitHub Actions / GitLab CI / Jenkins).
Generates automated continuous integration, unit testing, linting, and release build pipelines.
"""

from typing import Dict, Any

def generate_ci_cd_pipeline(
    provider: str = "GitHub Actions",
    language: str = "python",
    enable_docker: bool = True
) -> Dict[str, Any]:
    """
    Generates CI/CD pipeline YAML configuration.
    """
    prov_lower = provider.lower()
    
    yaml_config = f"""name: CI/CD Build & Test Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run Unit Tests
        run: |
          pytest --cov=core tests/

      - name: Run Code Linter
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
"""
    if enable_docker:
        yaml_config += """
      - name: Build Docker Image
        run: |
          docker build -t agent-app:latest .
"""

    return {
        "status": "success",
        "provider": provider,
        "language": language,
        "docker_support": enable_docker,
        "pipeline_file": ".github/workflows/ci.yml" if "github" in prov_lower else ".gitlab-ci.yml",
        "yaml_content": yaml_config
    }
