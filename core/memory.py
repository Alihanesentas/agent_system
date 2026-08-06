import os
from typing import List, Dict, Any, Tuple, Optional
from subagent_tracker.backend.tracker import count_tokens

class SlidingWindowMemory:
    """
    Sliding Window Context Memory Manager.
    Prunes old conversation turns in multi-turn agent dialogues to minimize prompt token usage,
    retaining only System Prompt + Brief Summary + Last N Active Messages.
    """
    def __init__(self, max_messages: int = 4, max_tokens: int = 2000):
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.history: List[Dict[str, str]] = []
        self.summary: str = ""

    def add_message(self, role: str, content: str):
        """Adds a message (user or assistant) to conversation history."""
        self.history.append({"role": role, "content": content})

    def clear(self):
        """Resets memory history and summary."""
        self.history = []
        self.summary = ""

    def get_pruned_context(
        self, 
        system_prompt: Optional[str] = None, 
        model_name: str = "gpt-4o"
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Builds a pruned context prompt.
        If history exceeds `max_messages`, older turns are compressed into a summary,
        saving up to 70-80% of prompt tokens in long multi-turn interactions.
        """
        full_raw_text = ""
        if system_prompt:
            full_raw_text += f"System: {system_prompt}\n"
        for msg in self.history:
            full_raw_text += f"{msg['role'].capitalize()}: {msg['content']}\n"

        original_tokens = count_tokens(full_raw_text, model_name)

        if len(self.history) <= self.max_messages:
            # Under limit: No pruning needed
            return full_raw_text.strip(), {
                "original_tokens": original_tokens,
                "pruned_tokens": original_tokens,
                "tokens_saved": 0,
                "savings_percent": 0.0,
                "pruned_count": 0
            }

        # Overflow: Keep last `max_messages` and summarize preceding turns
        old_turns = self.history[:-self.max_messages]
        recent_turns = self.history[-self.max_messages:]

        # Create lightweight summary of pruned turns
        pruned_summary_items = [f"{m['role']}:{m['content'][:30]}..." for m in old_turns]
        self.summary = "Pruned History Summary: " + " | ".join(pruned_summary_items)

        pruned_text = ""
        if system_prompt:
            pruned_text += f"System: {system_prompt}\n"
        pruned_text += f"[{self.summary}]\n"

        for msg in recent_turns:
            pruned_text += f"{msg['role'].capitalize()}: {msg['content']}\n"

        pruned_tokens = count_tokens(pruned_text, model_name)
        saved = max(0, original_tokens - pruned_tokens)
        savings_percent = round((saved / original_tokens * 100), 1) if original_tokens > 0 else 0.0

        metrics = {
            "original_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "tokens_saved": saved,
            "savings_percent": savings_percent,
            "pruned_count": len(old_turns)
        }

        return pruned_text.strip(), metrics
