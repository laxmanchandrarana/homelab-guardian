from datetime import datetime


class RestoreStatus:

    def __init__(self):
        self.jobs = {}

    def create(self, backup):
        job = {
            "backup": backup,
            "state": "QUEUED",
            "started": datetime.now(),
            "updated": datetime.now(),
            "error": None,
        }

        self.jobs[backup] = job
        return job

    def update(self, backup, state):
        if backup in self.jobs:
            self.jobs[backup]["state"] = state
            self.jobs[backup]["updated"] = datetime.now()

    def fail(self, backup, error):
        if backup in self.jobs:
            self.jobs[backup]["state"] = "FAILED"
            self.jobs[backup]["error"] = error
            self.jobs[backup]["updated"] = datetime.now()

    def get(self, backup):
        return self.jobs.get(backup)
