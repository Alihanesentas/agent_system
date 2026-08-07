"""Engine Sub-Package for Multi-Agent Pipelines, Simulations & LLM Fallback Smart Dispatch."""

from core.engine.llm_fallback import (
    smart_dispatch, search_engine_registry, list_all_engines,
    get_generated_scripts_list, generate_fallback_script, execute_generated_script,
    ENGINE_REGISTRY, KEYWORD_ALIASES
)
