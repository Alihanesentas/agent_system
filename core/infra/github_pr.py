"""
GitHub Pull Request & Branch Automation Module.
Automates creating feature branches, committing code, and opening GitHub Pull Requests 
via GitHub REST API or gh CLI.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from core.infra.git_ops import git_create_branch, git_auto_commit

def create_feature_branch_and_pr(
    branch_name: str,
    commit_message: str,
    pr_title: str,
    pr_body: str,
    base_branch: str = "main",
    repo_owner_repo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Automates creating a feature branch, staging/committing all changes, 
    and opening a GitHub Pull Request via GitHub REST API.
    """
    # 1. Create and switch to new branch
    branch_res = git_create_branch(branch_name)
    if branch_res.get("status") != "success":
        print(f"⚠️ Branch check: {branch_res.get('stdout', '')}")

    # 2. Auto-commit changes
    commit_res = git_auto_commit(commit_message)

    # 3. Create GitHub PR if token is available
    token = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")
    repo = repo_owner_repo or os.environ.get("GITHUB_REPOSITORY", "Alihanesentas/agent_system")

    if token:
        pr_res = _create_github_pr_api(repo, branch_name, base_branch, pr_title, pr_body, token)
        return {
            "status": "pr_created",
            "branch": branch_name,
            "commit": commit_res,
            "pr_url": pr_res.get("html_url", "N/A"),
            "pr_details": pr_res
        }

    return {
        "status": "branch_committed_locally",
        "branch": branch_name,
        "commit": commit_res,
        "note": "Provide GITHUB_TOKEN environment variable to automatically submit Pull Request to GitHub."
    }

def _create_github_pr_api(repo: str, head: str, base: str, title: str, body: str, token: str) -> Dict[str, Any]:
    """Creates a Pull Request via GitHub REST API (v3)."""
    url = f"https://api.github.com/repos/{repo}/pulls"
    payload = json.dumps({
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url, data=payload,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"Failed to create PR: {str(e)}"}
