"""
Async Job Queue & Worker Pool Module.
Manages background job submission, worker thread execution, job status tracking
(pending, running, completed, failed), and asynchronous result retrieval.
"""

import time
import uuid
import threading
from queue import Queue
from typing import Dict, Any, Optional

class JobStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AsyncWorkerQueue:
    def __init__(self, num_workers: int = 4):
        self.job_queue: Queue = Queue()
        self.results: Dict[str, Dict[str, Any]] = {}
        self.num_workers = num_workers
        self.workers: list = []
        self._start_workers()

    def _worker_loop(self):
        while True:
            job = self.job_queue.get()
            if job is None:
                break
            
            job_id = job["job_id"]
            func = job["func"]
            args = job.get("args", ())

            self.results[job_id]["status"] = JobStatus.RUNNING
            self.results[job_id]["started_at"] = time.time()

            try:
                out = func(*args)
                self.results[job_id]["status"] = JobStatus.COMPLETED
                self.results[job_id]["result"] = out
            except Exception as e:
                self.results[job_id]["status"] = JobStatus.FAILED
                self.results[job_id]["error"] = str(e)
            finally:
                self.results[job_id]["completed_at"] = time.time()
                self.job_queue.task_done()

    def _start_workers(self):
        for i in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

    def submit_job(self, func, *args) -> str:
        job_id = str(uuid.uuid4())[:8]
        self.results[job_id] = {
            "job_id": job_id,
            "status": JobStatus.PENDING,
            "submitted_at": time.time(),
            "result": None,
            "error": None
        }
        self.job_queue.put({"job_id": job_id, "func": func, "args": args})
        return job_id

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return self.results.get(job_id, {"status": "not_found"})

global_worker_queue = AsyncWorkerQueue(num_workers=4)
