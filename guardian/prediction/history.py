from collections import defaultdict, deque


class MetricsHistory:

    def __init__(self, window=60):
        self.window = window
        self.data = defaultdict(lambda: deque(maxlen=window))

    def add(self, service, metrics):
        self.data[service].append(metrics)

    def get(self, service):
        return list(self.data[service])

    def clear(self, service):
        self.data.pop(service, None)
