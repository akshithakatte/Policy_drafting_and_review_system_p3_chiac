from app import PolicyDraftingSystem

def main():
    """Demonstration of the Policy Drafting & Review System."""
    print("Policy Drafting & Review System Demo")
    print("=" * 50)

    system = PolicyDraftingSystem()

    # Demo with a sample policy topic
    topic = "Data Privacy Policy"
    requirements = """
    The policy should comply with GDPR and CCPA requirements.
    Include data collection, processing, storage, and user rights sections.
    Focus on employee responsibilities and breach response procedures.
    """

    print(f"Running demo for topic: {topic}")
    print(f"Requirements: {requirements.strip()}")

    # Run the workflow with 2 iterations
    final_policy = system.run_workflow(topic, requirements, iterations=2)

    print("\nDemo completed successfully!")
    print("Check the 'exports' directory for all generated files.")

if __name__ == "__main__":
    main()
