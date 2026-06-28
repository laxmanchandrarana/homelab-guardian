from datetime import datetime


class HealthCache:

    def __init__(self):
        self.cache = {}

    def record(self, service):

        entry = self.cache.setdefault(
            service,
            {
                "restarts": 0,
                "last": None,
            },
        )

        entry["restarts"] += 1
        entry["last"] = datetime.now()

    def get(self, service):

        return self.cache.get(
            service,
            {
                "restarts": 0,
                "last": None,
            },
        )

    def reset(self, service):

        self.cache.pop(service, None)
