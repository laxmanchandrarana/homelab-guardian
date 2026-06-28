from guardian.diagnostics.engine import DiagnosisEngine


class DiagnosisService:

    def __init__(self):
        self.engine = DiagnosisEngine()

    def diagnose(self, logs):
        return self.engine.diagnose(logs)
