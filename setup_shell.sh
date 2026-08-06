#!/usr/bin/env bash
# Shell environment setup script for Zsh and Bash.
# Source this file (`source setup_shell.sh`) or add it to ~/.zshrc

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Global Terminal Aliases
alias agent="python3 $PROJECT_DIR/agent.py"
alias agent-stats="sqlite3 -header -column $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT COUNT(*) as Calls, SUM(prompt_tokens) as Prompt, SUM(completion_tokens) as Output, SUM(total_tokens) as Total, PRINTF(\"\$%.6f\", SUM(estimated_cost_usd)) as Cost FROM agentlog;'"
alias agent-logs="sqlite3 -header -column $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT id, DATETIME(created_at) as Time, agent_name, model_name, total_tokens, PRINTF(\"\$%.6f\", estimated_cost_usd) as Cost FROM agentlog ORDER BY id DESC LIMIT 10;'"
alias agent-watch="while true; do clear; date; agent-stats; echo ''; agent-logs; sleep 2; done"
alias agent-export="sqlite3 -header -csv $PROJECT_DIR/subagent_tracker/backend/tracker.db 'SELECT * FROM agentlog;' > token_export.csv && echo '✅ Exported to token_export.csv'"

echo "⚡ Agent System Terminal Environment Loaded!"
echo "Available Terminal Commands & Aliases:"
echo "  • agent         -> Launches interactive Gemini/Claude style agent CLI shell"
echo "  • agent-stats   -> Single-line shell command to view token & cost summary"
echo "  • agent-logs    -> Single-line shell command to view recent logs"
echo "  • agent-watch   -> Single-line live terminal monitoring loop"
echo "  • agent-export  -> Single-line shell command to export CSV"
