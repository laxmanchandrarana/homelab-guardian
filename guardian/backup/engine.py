import subprocess
from pathlib import Path
from datetime import datetime
from guardian.repositories.backup_repo import BackupRepository

BACKUP_ROOT = Path("/mnt/storage/Backup/backups")
repo = BackupRepository()

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

        cmd = (
            f"sudo /usr/bin/tar "
            f"--warning=no-file-changed "
            f"-czpf {filename} "
            f"/home/sonjoy/server-services"
        )

        return self.run(cmd)

    def sha256(path: Path):
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()
