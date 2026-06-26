import hashlib
import shutil
import tarfile
from pathlib import Path


class VerifyEngine:

    def checksum(self, file: Path):
        sha = hashlib.sha256()

        with open(file, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                sha.update(chunk)

        return sha.hexdigest()

    def integrity(self, file: Path):
        try:
            with tarfile.open(file, "r:gz") as tar:
                tar.getmembers()
            return True
        except Exception:
            return False

    def disk_ok(self, file: Path):
        free = shutil.disk_usage("/").free
        return free > file.stat().st_size

    def verify(self, file: Path):

        if not file.exists():
            return {
                "ok": False,
                "reason": "Backup not found"
            }

        return {
            "ok": True,
            "size": file.stat().st_size,
            "sha256": self.checksum(file),
            "integrity": self.integrity(file),
            "disk_ok": self.disk_ok(file)
        }
