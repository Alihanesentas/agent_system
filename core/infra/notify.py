"""
Webhook & Notification System — Slack, Discord, and Telegram Alerts.
Sends notifications when agent tasks complete, errors occur, or builds finish.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from datetime import datetime

def send_slack_notification(message: str, webhook_url: Optional[str] = None) -> Dict[str, Any]:
    """Sends a notification to Slack via Incoming Webhook."""
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL", "")
    if not url:
        return {"status": "skipped", "reason": "SLACK_WEBHOOK_URL not configured."}

    payload = json.dumps({
        "text": message,
        "username": "Agent System",
        "icon_emoji": ":robot_face:"
    }).encode("utf-8")

    return _send_webhook(url, payload)

def send_discord_notification(message: str, webhook_url: Optional[str] = None) -> Dict[str, Any]:
    """Sends a notification to Discord via Webhook."""
    url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not url:
        return {"status": "skipped", "reason": "DISCORD_WEBHOOK_URL not configured."}

    payload = json.dumps({
        "content": message,
        "username": "Agent System 🤖"
    }).encode("utf-8")

    return _send_webhook(url, payload)

def send_telegram_notification(message: str, bot_token: Optional[str] = None, chat_id: Optional[str] = None) -> Dict[str, Any]:
    """Sends a notification to Telegram via Bot API."""
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    cid = chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not cid:
        return {"status": "skipped", "reason": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured."}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": cid,
        "text": message,
        "parse_mode": "Markdown"
    }).encode("utf-8")

    return _send_webhook(url, payload)

def notify_all(message: str) -> Dict[str, Any]:
    """Sends notification to all configured channels (Slack, Discord, Telegram)."""
    results = {}
    results["slack"] = send_slack_notification(message)
    results["discord"] = send_discord_notification(message)
    results["telegram"] = send_telegram_notification(message)
    return results

def notify_task_complete(agent_name: str, task_summary: str, elapsed_ms: float, status: str = "success"):
    """Convenience function to notify about a completed agent task."""
    emoji = "✅" if status == "success" else "❌"
    msg = (
        f"{emoji} *Agent Task Completed*\n"
        f"• Agent: `{agent_name}`\n"
        f"• Status: {status}\n"
        f"• Duration: {elapsed_ms:.0f}ms\n"
        f"• Summary: {task_summary[:200]}\n"
        f"• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return notify_all(msg)

def _send_webhook(url: str, payload: bytes) -> Dict[str, Any]:
    """Internal helper to send JSON payload to a webhook URL."""
    try:
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return {"status": "sent", "http_code": response.status}
    except urllib.error.HTTPError as e:
        return {"status": "error", "http_code": e.code, "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
