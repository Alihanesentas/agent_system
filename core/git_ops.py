"""
Git Automation — Automated Commit, Branch, Diff, and Status Operations.
Provides the agent with safe git operations for version control automation.
"""

import os
from typing import Dict, Any, Optional, List
from core.executor import execute_command

def git_status(cwd: str = ".") -> Dict[str, Any]:
    """Returns current git status (staged, unstaged, untracked files)."""
    return execute_command("git status --porcelain", cwd=cwd)

def git_diff(file_path: Optional[str] = None, cwd: str = ".") -> Dict[str, Any]:
    """Shows git diff for a specific file or all changes."""
    cmd = f"git diff {file_path}" if file_path else "git diff"
    return execute_command(cmd, cwd=cwd)

def git_log(n: int = 10, cwd: str = ".") -> Dict[str, Any]:
    """Returns recent git log entries."""
    return execute_command(f"git log --oneline -n {n}", cwd=cwd)

def git_branch(cwd: str = ".") -> Dict[str, Any]:
    """Lists all branches and highlights current branch."""
    return execute_command("git branch -a", cwd=cwd)

def git_add(files: str = ".", cwd: str = ".") -> Dict[str, Any]:
    """Stages files for commit."""
    return execute_command(f"git add {files}", cwd=cwd)

def git_commit(message: str, cwd: str = ".") -> Dict[str, Any]:
    """Creates a git commit with the given message."""
    # Escape quotes in message
    safe_msg = message.replace('"', '\\"')
    return execute_command(f'git commit -m "{safe_msg}"', cwd=cwd)

def git_auto_commit(message: str, files: str = ".", cwd: str = ".") -> Dict[str, Any]:
    """Stages all changes and commits in one operation."""
    add_result = git_add(files, cwd)
    if add_result.get("status") != "success":
        return add_result
    return git_commit(message, cwd)

def git_create_branch(branch_name: str, cwd: str = ".") -> Dict[str, Any]:
    """Creates and switches to a new branch."""
    return execute_command(f"git checkout -b {branch_name}", cwd=cwd)

def git_stash(action: str = "push", cwd: str = ".") -> Dict[str, Any]:
    """Stashes or pops changes (actions: push, pop, list)."""
    return execute_command(f"git stash {action}", cwd=cwd)
