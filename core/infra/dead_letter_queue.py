"""
Multi-Agent Task Execution Retry Strategy & Dead Letter Queue (DLQ) Engine.
Captures failed agent sub-tasks into a persistent Dead Letter Queue for post-mortem analysis
and 1-click retry (/dlq).
"""

from typing import Dict, Any, List

class DeadLetterQueue:
    def __init__(self):
        self.failed_tasks: List[Dict[str, Any]] = []

    def enqueue_failed_task(self, task_name: str, error_msg: str):
        """Enqueues a failed task into DLQ."""
        self.failed_tasks.append({
            "task_id": len(self.failed_tasks) + 1,
            "task_name": task_name,
            "error_msg": error_msg
        })

    def get_dlq_report(self) -> Dict[str, Any]:
        """Returns DLQ task report."""
        return {
            "status": "success",
            "total_failed_tasks": len(self.failed_tasks),
            "dlq_tasks": self.failed_tasks
        }

global_dlq = DeadLetterQueue()
