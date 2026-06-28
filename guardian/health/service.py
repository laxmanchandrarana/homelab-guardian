from guardian.health.cache import HealthCache
from guardian.health.policy import HealthPolicy

cache = HealthCache()


class HealthService:

    def __init__(self):

        self.policy = HealthPolicy()

    def can_restart(self, service):

        history = cache.get(service)

        return self.policy.allow_restart(history)

    def restarted(self, service):

        cache.record(service)

    def healed(self, service):

        cache.reset(service)
