from pathlib import Path
import tarfile


class RestorePlanner:

    def analyze(self, archive: Path):

        if not archive.exists():
            raise FileNotFoundError(archive)

        files = []

        size = 0

        with tarfile.open(archive, "r:gz") as tar:

            for member in tar.getmembers():

                files.append(member.name)

                size += member.size

        return {
            "backup": archive.name,
            "files": len(files),
            "size": size,
            "preview": files[:20]
        }

