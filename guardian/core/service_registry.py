import yaml

from guardian.settings import CONFIG_DIR


class ServiceRegistry:

    def __init__(self):

        self.services = {}

        self.load()

    def load(self):

        with open(CONFIG_DIR / "services.yml") as f:

            self.services = yaml.safe_load(f)["services"]

    def get(self, name):

        return self.services.get(name)

    def list(self):

        return self.services
