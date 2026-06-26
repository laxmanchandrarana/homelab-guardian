from pathlib import Path
import subprocess

BACKUP_DIR = Path("/mnt/storage/Backup/backups")


class RestoreEngine:

    def backups(self):
        return sorted(BACKUP_DIR.glob("*.tar.gz"))

    def restore(self, filename):
        backup = BACKUP_DIR / filename

        return subprocess.run(
            [
                "sudo",
                "/home/sonjoy/projects/homelab-guardian/guardian/scripts/restore.sh",
                str(backup)
            ],
            capture_output=True,
            text=True
        )
