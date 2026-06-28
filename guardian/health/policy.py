from pathlib import Path

import yaml


class HealthPolicy:

    def __init__(self):
        self.config = self._load()

    def _load(self):
        config_file = Path("guardian/config.yaml")

        if not config_file.exists():
            return {
                "services": {},
                "restart_limit": 3,
            }

        with open(config_file, "r") as f:
            data = yaml.safe_load(f) or {}

        data.setdefault("services", {})
        data.setdefault("restart_limit", 3)

        return data

    def is_enabled(self, service: str) -> bool:
        services = self.config.get("services", {})

        return services.get(service, {}).get("enabled", True)

    def allow_restart(self, history) -> bool:
        limit = self.config.get("restart_limit", 3)

        return len(history) < limit

    def reload(self):
        self.config = self._load()
