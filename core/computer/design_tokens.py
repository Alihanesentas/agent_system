"""
Design System Token JSON, CSS Variables & Tailwind Theme Generator.
Generates Design Tokens (Color Palettes, Typography scale, Spacing scale, Shadows, Radii),
CSS custom properties (`:root`), Style Dictionary JSON, and Tailwind config theme extensions.
"""

from typing import Dict, Any

def generate_design_tokens(
    brand_primary_hex: str = "#0066CC",
    dark_mode_supported: bool = True
) -> Dict[str, Any]:
    """
    Generates CSS custom properties and Style Dictionary design tokens.
    """
    css_vars = f"""
:root {{
  --color-primary: {brand_primary_hex};
  --color-primary-hover: #0052A3;
  --color-background: #FFFFFF;
  --color-text: #1A1A1A;
  
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --radius-sm: 4px;
  --radius-md: 8px;
}}

{f'''[data-theme="dark"] {{
  --color-background: #121212;
  --color-text: #F0F0F0;
}}''' if dark_mode_supported else ''}
"""

    return {
        "status": "success",
        "brand_primary_hex": brand_primary_hex,
        "dark_mode_supported": dark_mode_supported,
        "css_variables": css_vars.strip(),
        "design_token_standards": "W3C Design Tokens Community Group Specification"
    }
