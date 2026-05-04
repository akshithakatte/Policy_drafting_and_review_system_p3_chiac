import os
from datetime import datetime
from agents.policy_drafter import PolicyDrafter
from agents.legal_reviewer import LegalReviewer
from agents.risk_auditor import RiskAuditor
from agents.reviser import Reviser
from agents.validation_checklist import ValidationChecklist
from utils.diff_viewer import DiffViewer
from utils.file_exporter import FileExporter

class PolicyDraftingSystem:
    def __init__(self):
        self.drafter = PolicyDrafter()
        self.legal_reviewer = LegalReviewer()
        self.risk_auditor = RiskAuditor()
        self.reviser = Reviser()
        self.validator = ValidationChecklist()
        self.diff_viewer = DiffViewer()
        self.exporter = FileExporter()

    def run_workflow(self, topic, requirements=None, iterations=1):
        """Run the complete policy drafting and review workflow."""
        print(f"Starting policy drafting workflow for: {topic}")
        print("=" * 60)

        # Step 1: Initial Drafting
        print("1. Drafting initial policy...")
        policy = self.drafter.draft_policy(topic, requirements)
        self.exporter.export_policy(policy, f"{topic.replace(' ', '_')}_draft", 0)
        print("   Initial draft completed and exported.")

        current_policy = policy

        for iteration in range(1, iterations + 1):
            print(f"\nIteration {iteration}:")
            print("-" * 40)

            # Step 2: Legal Review
            print("2. Conducting legal review...")
            legal_feedback = self.legal_reviewer.review_policy(current_policy)
            self.exporter.export_feedback(legal_feedback, "legal", topic.replace(' ', '_'))
            print("   Legal review completed and exported.")

            # Step 3: Risk Audit
            print("3. Performing risk audit...")
            risk_feedback = self.risk_auditor.audit_policy(current_policy)
            self.exporter.export_feedback(risk_feedback, "risk", topic.replace(' ', '_'))
            print("   Risk audit completed and exported.")

            # Step 4: Revision
            print("4. Revising policy based on feedback...")
            revised_policy = self.reviser.revise_policy(current_policy, legal_feedback, risk_feedback)
            self.exporter.export_policy(revised_policy, f"{topic.replace(' ', '_')}_revised", iteration)
            print("   Policy revision completed and exported.")

            # Step 5: Generate Diff
            print("5. Generating policy diff...")
            diff_text, diff_html = self.diff_viewer.generate_diff(current_policy, revised_policy)
            self.exporter.export_diff(diff_html, f"{topic.replace(' ', '_')}_iteration_{iteration}")
            print("   Diff generated and exported.")

            current_policy = revised_policy

        # Step 6: Final Validation
        print("\n6. Final validation...")
        checklist = self.validator.generate_checklist(topic)
        validation_report = self.validator.validate_policy(current_policy, checklist)
        self.exporter.export_validation_report(validation_report, topic.replace(' ', '_'))
        print("   Final validation completed and exported.")

        print("\n" + "=" * 60)
        print("Policy drafting workflow completed!")
        print(f"All files exported to: {self.exporter.export_dir}")
        print("=" * 60)

        return current_policy

def main():
    system = PolicyDraftingSystem()

    # Example usage - you can modify this for different topics
    topic = input("Enter policy topic: ").strip()
    requirements = input("Enter any specific requirements (or press Enter for none): ").strip()
    requirements = requirements if requirements else None

    final_policy = system.run_workflow(topic, requirements)

    print("\nFinal Policy Preview:")
    print("-" * 30)
    print(final_policy[:500] + "..." if len(final_policy) > 500 else final_policy)

if __name__ == "__main__":
    main()
