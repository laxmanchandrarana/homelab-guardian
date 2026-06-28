from datetime import datetime

from guardian.restore.executor import RestoreExecutor
from guardian.restore.jobs import RestoreJobs
from guardian.restore.health import RestoreHealth

from guardian.repositories.restore_repo import RestoreRepository
from guardian.repositories.audit_repo import AuditRepository

from guardian.models.restore import Restore
from guardian.models.audit import Audit

from guardian.restore.rollback import RollbackService

class RestoreService:

    def __init__(self):

        self.executor = RestoreExecutor()

        self.jobs = RestoreJobs()

        self.health = RestoreHealth()

        self.repo = RestoreRepository()

        self.audit = AuditRepository()

        self.rollback = RollbackService()

    def run(self, filename):

        self.jobs.create(filename)
        self.jobs.update(filename, "RUNNING")

        started = datetime.now()

        result = self.executor.execute(filename)

        # -------------------------------
        # Health verification
        # -------------------------------
        report = self.health.check()

        completed = datetime.now()

        rollback = None

        if result["returncode"] == 0 and report["healthy"]:
            status = "SUCCESS"
        else:
            status = "FAILED"

            self.jobs.update(filename, "ROLLING_BACK")

            rollback = self.rollback.rollback(filename)

        # Save restore history
        self.repo.add(
            Restore(
                filename=filename,
                started=started,
                completed=completed,
                status=status,
            )
        )

        # Save audit log
        self.audit.add(
            Audit(
                created=completed,
                action=f"RESTORE_{status}",
                user="system",
                details=filename,
            )
        )

        # Update job state
        self.jobs.update(filename, status)

        return {
            "job": self.jobs.get(filename),
            "health": report,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "returncode": result["returncode"],
            "rollback": rollback,
        }
