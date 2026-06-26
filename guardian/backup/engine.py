import subprocess
from pathlib import Path
from datetime import datetime


BACKUP_ROOT = Path("/mnt/storage/Backup/backups")


class BackupEngine:

    def create_directory(self):

        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    def timestamp(self):

        return datetime.now().strftime("%Y%m%d-%H%M%S")

    def run(self, command):

        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )

    def docker_backup(self):

        self.create_directory()

        filename = BACKUP_ROOT / f"docker-{self.timestamp()}.tar.gz"

        cmd = f"tar czf {filename} /home/sonjoy/server-services"

        return self.run(cmd)
