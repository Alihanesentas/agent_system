#!/usr/bin/env bash
# Shell environment setup script for Zsh and Bash.
# Source this file (`source setup_shell.sh`) or add it to ~/.zshrc

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python3"

if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

# Global Terminal Aliases
alias agent="$PYTHON_BIN $PROJECT_DIR/agent.py"
alias agent-stats="sqlite3 -header -column $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT COUNT(*) as Calls, SUM(prompt_tokens) as Prompt, SUM(completion_tokens) as Output, SUM(total_tokens) as Total, PRINTF(\"\$%.6f\", SUM(estimated_cost_usd)) as Cost FROM agentlog;'"
alias agent-logs="sqlite3 -header -column $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT id, DATETIME(created_at) as Time, agent_name, model_name, total_tokens, PRINTF(\"\$%.6f\", estimated_cost_usd) as Cost FROM agentlog ORDER BY id DESC LIMIT 10;'"
alias agent-watch="while true; do clear; date; agent-stats; echo ''; agent-logs; sleep 2; done"
alias agent-export="sqlite3 -header -csv $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT * FROM agentlog;' > token_export.csv && echo '✅ Exported to token_export.csv'"

# Auto-install to ~/.zshrc if requested or run standalone
if [ "$1" == "--install" ] || [ "$1" == "-i" ]; then
    ZSHRC="$HOME/.zshrc"
    SOURCE_LINE="source \"$PROJECT_DIR/setup_shell.sh\""
    if [ -f "$ZSHRC" ]; then
        if ! grep -q "$PROJECT_DIR/setup_shell.sh" "$ZSHRC"; then
            echo "" >> "$ZSHRC"
            echo "# Multi-Agent System Shell Integration" >> "$ZSHRC"
            echo "$SOURCE_LINE" >> "$ZSHRC"
            echo "✅ 'agent' komutu ~/.zshrc dosyasına eklendi!"
        else
            echo "ℹ️ 'agent' komutu zaten ~/.zshrc içinde tanımlı."
        fi
    fi
fi

echo "⚡ Agent System Terminal Environment Loaded!"
echo "Available Terminal Commands & Aliases:"
echo "  • agent         -> Launches interactive Gemini/Claude style agent CLI shell"
echo "  • agent-stats   -> Single-line shell command to view token & cost summary"
echo "  • agent-logs    -> Single-line shell command to view recent logs"
echo "  • agent-watch   -> Single-line live terminal monitoring loop"
echo "  • agent-export  -> Single-line shell command to export CSV"
