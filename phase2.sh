# Create all required directories at once
mkdir -p guardian/core guardian/services guardian/cli .github/workflows

# Phase 2.2 — Guardian Service Registry
touch guardian/core/__init__.py

cat << 'EOF' > guardian/core/service_registry.py
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
EOF

# Phase 2.3 — Docker Manager
cat << 'EOF' > guardian/services/docker_service.py
import docker

client = docker.from_env()


class DockerService:

    def list(self):

        return client.containers.list(all=True)

    def restart(self, name):

        client.containers.get(name).restart()

    def stop(self, name):

        client.containers.get(name).stop()

    def start(self, name):

        client.containers.get(name).start()

    def logs(self, name):

        return client.containers.get(name).logs().decode()
EOF

# Phase 2.4 — Health Engine
cat << 'EOF' > guardian/core/health.py
import psutil


class Health:

    def cpu(self):

        return psutil.cpu_percent(interval=1)

    def memory(self):

        return psutil.virtual_memory().percent

    def disk(self):

        return psutil.disk_usage("/").percent

    def boot(self):

        return psutil.boot_time()
EOF

# Phase 2.5 — Event Bus
cat << 'EOF' > guardian/core/eventbus.py
class EventBus:

    def __init__(self):

        self.listeners = {}

    def on(self, event, callback):

        self.listeners.setdefault(event, []).append(callback)

    def emit(self, event, data):

        for cb in self.listeners.get(event, []):

            cb(data)
EOF

# Phase 2.6 — Scheduler
cat << 'EOF' > guardian/core/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def start():

    scheduler.start()
EOF

# Phase 2.7 — Configuration Loader
cat << 'EOF' > guardian/core/config_loader.py
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
EOF

# Phase 2.8 — Guardian CLI
cat << 'EOF' > guardian/cli/main.py
import typer

app = typer.Typer()


@app.command()
def doctor():
    print("Running Guardian Doctor...")


@app.command()
def backup():
    print("Running Backup...")


@app.command()
def restore():
    print("Running Restore...")


@app.command()
def restart(service: str):
    print(f"Restarting {service}")


if __name__ == "__main__":
    app()
EOF

# Phase 2.9 — GitHub Actions (Placeholder setup)
cat << 'EOF' > .github/workflows/python.yml
name: Guardian CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-packages: '3.11'
EOF

echo "✅ Guardian infrastructure files successfully created!"
