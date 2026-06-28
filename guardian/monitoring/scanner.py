from guardian.services.docker_service import DockerService


class DockerScanner:

    def __init__(self):
        self.docker = DockerService()

    def scan(self):
        return self.docker.list()
