from guardian.ai.collector import LogCollector
from guardian.ai.analyzer import FailureAnalyzer
from guardian.ai.advisor import RecoveryAdvisor


class AIService:

    def __init__(self):
        self.collector = LogCollector()
        self.analyzer = FailureAnalyzer()
        self.advisor = RecoveryAdvisor()

    def analyze(self, service):

        data = self.collector.collect(service)

        analysis = self.analyzer.analyze(data)

        recommendation = self.advisor.recommend(analysis)

        return {
            "collector": data,
            "analysis": analysis,
            "recommendation": recommendation,
        }
