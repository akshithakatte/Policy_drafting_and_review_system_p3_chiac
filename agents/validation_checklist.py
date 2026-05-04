from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class ValidationChecklist:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL
        self.system_prompt = """
        You are a compliance validation expert. Your task is to create and validate policies against
        comprehensive checklists covering:
        - Legal compliance
        - Regulatory requirements
        - Industry standards
        - Best practices
        - Operational feasibility

        Provide detailed checklists and validation reports.
        """

    def generate_checklist(self, policy_topic):
        """Generate a comprehensive validation checklist for the policy topic."""
        prompt = f"""
        {self.system_prompt}

        Policy Topic: {policy_topic}

        Create a detailed validation checklist that should be used to assess policy compliance.
        Structure the checklist with categories and specific items to verify.

        Format as a clear, actionable checklist with checkboxes or verification points.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()

    def validate_policy(self, policy_text, checklist):
        """Validate the policy against the checklist and provide a validation report."""
        prompt = f"""
        {self.system_prompt}

        Policy to Validate:
        {policy_text}

        Validation Checklist:
        {checklist}

        Please validate the policy against the checklist. Provide:
        1. Checklist item-by-item validation
        2. Overall compliance score
        3. Areas of strength
        4. Areas needing improvement
        5. Recommendations for full compliance

        Be thorough and specific in your assessment.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content.strip()
