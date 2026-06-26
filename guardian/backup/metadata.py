from pathlib import Path
from datetime import datetime
import hashlib


class BackupMetadata:

    def filename(self, path: Path):
        return path.name

    def filesize(self, path: Path):
        return path.stat().st_size

    def created(self, path: Path):
        return datetime.fromtimestamp(path.stat().st_ctime)

    def sha256(self, path: Path):
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()
