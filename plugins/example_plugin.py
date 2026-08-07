"""Example Plugin — Template for creating custom agent plugins."""

from core.plugins import register_plugin

def my_custom_tool(input_text: str) -> str:
    """Your custom tool logic here."""
    return f"Processed: {input_text}"

def register():
    """Called automatically when plugins are loaded."""
    register_plugin(
        name="example_tool",
        description="A sample plugin template for demonstration",
        handler=my_custom_tool,
        category="tool"
    )
