from setuptools import setup, find_packages

setup(
    name="agent-system",
    version="1.2.0",
    packages=find_packages(),
    py_modules=["agent", "mcp_server"],
    install_requires=[
        "requests",
        "pydantic",
        "fastapi",
        "uvicorn",
        "rich",
        "chromadb"
    ],
    entry_points={
        "console_scripts": [
            "agent=agent:main",
        ],
    },
)
