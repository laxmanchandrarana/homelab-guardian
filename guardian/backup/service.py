from pathlib import Path

from guardian.backup.engine import BackupEngine
from guardian.repositories.backup_repo import BackupRepository


BACKUP_ROOT = Path("/mnt/storage/Backup/backups")


class BackupService:

    def __init__(self):
        self.engine = BackupEngine()
        self.repo = BackupRepository()

    def run(self):

        result = self.engine.docker_backup()

        backups = sorted(
            BACKUP_ROOT.glob("*.tar.gz"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )

        if backups:

            newest = backups[0]

            self.repo.create(
                filename=newest.name,
                size=newest.stat().st_size,
                status="SUCCESS" if result.returncode == 0 else "FAILED",
            )

        return result
