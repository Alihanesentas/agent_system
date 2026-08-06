#!/usr/bin/env bash
# Shell environment setup script for Zsh and Bash.
# Source this file (`source setup_shell.sh`) or add it to ~/.zshrc

# Robust absolute directory resolution across Zsh and Bash
if [ -n "$ZSH_VERSION" ]; then
    PROJECT_DIR="$(cd "$(dirname "${(%):-%x}")" 2>/dev/null && pwd)"
else
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
fi

# Safety fallback to exact project path
if [ -z "$PROJECT_DIR" ] || [ "$PROJECT_DIR" = "$HOME" ] || [ ! -f "$PROJECT_DIR/agent.py" ]; then
    PROJECT_DIR="/Users/alihanesentas/Desktop/agent_system"
fi

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

echo "⚡ Agent System Terminal Environment Loaded!"
echo "Project Dir: $PROJECT_DIR"
echo "Available Terminal Commands & Aliases:"
echo "  • agent         -> Launches interactive Gemini/Claude style agent CLI shell"
echo "  • agent-stats   -> Single-line shell command to view token & cost summary"
echo "  • agent-logs    -> Single-line shell command to view recent logs"
echo "  • agent-watch   -> Single-line live terminal monitoring loop"
echo "  • agent-export  -> Single-line shell command to export CSV"
