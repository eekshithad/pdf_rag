from services.report_service import ReportService


class ReportAgent:

    def __init__(self):

        self.service = ReportService()

    def run(self, topic):

        report = self.service.generate_report(topic)

        return report