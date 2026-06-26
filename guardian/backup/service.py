from guardian.backup.engine import BackupEngine
from guardian.repositories.backup_repo import BackupRepository
from guardian.models.backup import Backup
from guardian.repositories.audit_repo import AuditRepository
from guardian.models.audit import Audit


class BackupService:

    def __init__(self):
        self.engine = BackupEngine()
        self.repo = BackupRepository()
        self.audit = AuditRepository()

    def run(self):
        result = self.engine.docker_backup()
        process = result["process"]

        if "filename" in result:
            status = "SUCCESS" if process.returncode == 0 else "FAILED"

            backup = Backup(
                filename=result["filename"],
                sha256=result["sha256"],
                size=result["size"],
                created=result["created"],
                verified=False,
                location=str(result["path"]),
                status=status,
            )
            self.repo.add(backup)

            audit = Audit(
                action=f"BACKUP_{status}",
                resource=result["filename"],
                status=status,
            )
            self.audit.add(audit)

        return process
