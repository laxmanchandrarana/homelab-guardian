import docker

client = docker.from_env()


class DockerService:

    def list(self):
        return [
            {
                "id": c.id,
                "name": c.name,
                "status": c.status,
            }
            for c in client.containers.list(all=True)
        ]

    def containers(self):
        return client.containers.list(all=True)

    def get(self, name):
        return client.containers.get(name)

    def start(self, name):
        self.get(name).start()

    def stop(self, name):
        self.get(name).stop()

    def restart(self, name):
        self.get(name).restart()

    def remove(self, name):
        self.get(name).remove(force=True)

    def logs(self, name, tail=100):
        return self.get(name).logs(tail=tail).decode()

    def stats(self, name):
        return self.get(name).stats(stream=False)

    def inspect(self, name):
        return self.get(name).attrs
