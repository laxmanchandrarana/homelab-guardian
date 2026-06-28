class StateCache:

    def __init__(self):
        self.states = {}

    def changed(self, service, status):
        previous = self.states.get(service)

        if previous == status:
            return False

        self.states[service] = status
        return True


state_cache = StateCache()
