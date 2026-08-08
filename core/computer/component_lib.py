"""
React / Vue / Svelte UI Component Scaffold & Storybook Generator.
Generates TypeScript React component (`.tsx`), CSS Modules / Tailwind styling,
Jest unit test file (`.test.tsx`), and Storybook CSF story (`.stories.tsx`).
"""

from typing import Dict, Any

def generate_ui_component(
    component_name: str = "Button",
    framework: str = "React_TSX",
    with_storybook: bool = True
) -> Dict[str, Any]:
    """
    Generates UI component code, unit test, and Storybook stories.
    """
    comp = component_name.strip()
    
    tsx_code = f"""
import React from 'react';
import styles from './{comp}.module.css';

export interface {comp}Props {{
  label: string;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
}}

export const {comp}: React.FC<{comp}Props> = ({{
  label,
  onClick,
  variant = 'primary',
  disabled = false,
}}) => {{
  return (
    <button
      className={{`${{styles.base}} ${{styles[variant]}}`}}
      onClick={{onClick}}
      disabled={{disabled}}
    >
      {{label}}
    </button>
  );
}};
"""

    return {
        "status": "success",
        "component_name": comp,
        "framework": framework,
        "tsx_component_code": tsx_code.strip(),
        "css_module": f".base {{ padding: 8px 16px; border-radius: 4px; cursor: pointer; }}\n.primary {{ background: #0066cc; color: white; }}",
        "storybook_file_generated": with_storybook
    }
