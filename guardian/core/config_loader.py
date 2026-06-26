import yaml

from guardian.settings import CONFIG_DIR


class Config:

    def __init__(self):

        self.cache = {}

    def get(self, file):

        if file not in self.cache:

            with open(CONFIG_DIR / file) as f:

                self.cache[file] = yaml.safe_load(f)

        return self.cache[file]
