from pathlib import Path
import yaml

from guardian.settings import CONFIG_DIR


def load(filename):

    path = CONFIG_DIR / filename

    with open(path, "r") as f:
        return yaml.safe_load(f)
