import threading
import time
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, func, interval_seconds, *args, **kwargs):
        """
        Schedule a function to run every interval_seconds
        """
        job = threading.Thread(target=self._job_runner, args=(func, interval_seconds, args, kwargs), daemon=True)
        self.jobs.append(job)
        job.start()

    def _job_runner(self, func, interval, args, kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Scheduler error: {str(e)}")
            time.sleep(interval)

    def list_jobs(self):
        return [f"Job {i+1}" for i in range(len(self.jobs))]
