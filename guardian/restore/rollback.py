from pathlib import Path

from guardian.restore.executor import RestoreExecutor
from guardian.repositories.backup_repo import BackupRepository


class RollbackService:

    def __init__(self):
        self.repo = BackupRepository()
        self.executor = RestoreExecutor()

    def rollback(self, failed_backup):

        backups = self.repo.list()

        previous = None

        for backup in backups:

            if backup.filename == failed_backup:
                continue

            if backup.status == "SUCCESS":
                previous = backup
                break

        if previous is None:
            return {
                "success": False,
                "reason": "No previous successful backup found",
            }

        result = self.executor.execute(previous.filename)

        return {
            "success": result["returncode"] == 0,
            "backup": previous.filename,
            "result": result,
        }
