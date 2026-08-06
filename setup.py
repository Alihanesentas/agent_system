from setuptools import setup, find_packages

setup(
    name="agent-system",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["agent", "cli"],
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "tiktoken",
        "peewee",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "agent=agent:main",
            "agent-tracer=cli:main"
        ],
    },
    python_requires=">=3.9",
)
