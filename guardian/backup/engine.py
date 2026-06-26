import subprocess
from pathlib import Path
from datetime import datetime
from guardian.backup.metadata import BackupMetadata

BACKUP_ROOT = Path("/mnt/storage/Backup/backups")
metadata = BackupMetadata()


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
            f"--ignore-failed-read "
            f"-czpf {filename} "
            f"/home/sonjoy/server-services"
        )

        result = self.run(cmd)

        data = {
            "process": result,
            "path": filename,
        }

        if filename.exists():
            data["filename"] = metadata.filename(filename)
            data["size"] = metadata.filesize(filename)
            data["created"] = metadata.created(filename)
            data["sha256"] = metadata.sha256(filename)

        return data
