from pathlib import Path

PLUGIN_DIR = Path("guardian/plugins")


def discover():

    return [x.name for x in PLUGIN_DIR.iterdir() if x.is_dir()]

