from guardian.prediction.history import MetricsHistory
from guardian.prediction.analyzer import TrendAnalyzer

import psutil


class PredictionService:

    def __init__(self):
        self.history = MetricsHistory(window=10)
        self.analyzer = TrendAnalyzer()

    def metrics(self):
        """Collect current system metrics."""

        return {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
        }

    def predict(self, service):

        sample = self.metrics()

        self.history.add(service, sample)

        history = self.history.get(service)

        analysis = self.analyzer.analyze(history)

        return {
            "service": service,
            "current": sample,
            "history": history,
            "prediction": analysis,
        }
