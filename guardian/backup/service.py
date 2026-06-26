from guardian.backup.engine import BackupEngine


class BackupService:

    def __init__(self):
        self.engine = BackupEngine()

    def run(self):

        return self.engine.docker_backup()
