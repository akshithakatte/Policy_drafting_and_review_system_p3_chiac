import os
from datetime import datetime

class FileExporter:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_policy(self, policy_text, filename, iteration=None):
        """Export policy text to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if iteration is not None:
            filename = f"{filename}_iteration_{iteration}_{timestamp}.txt"
        else:
            filename = f"{filename}_{timestamp}.txt"

        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(policy_text)
        return filepath

    def export_feedback(self, feedback_text, feedback_type, policy_topic):
        """Export feedback (legal, risk, etc.) to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{policy_topic}_{feedback_type}_feedback_{timestamp}.txt"
        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(feedback_text)
        return filepath

    def export_diff(self, diff_html, policy_topic):
        """Export HTML diff to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{policy_topic}_diff_{timestamp}.html"
        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(diff_html)
        return filepath

    def export_validation_report(self, report_text, policy_topic):
        """Export validation report to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{policy_topic}_validation_report_{timestamp}.txt"
        filepath = os.path.join(self.export_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return filepath
