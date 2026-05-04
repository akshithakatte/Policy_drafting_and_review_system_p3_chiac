from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class LegalReviewer:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL
        self.system_prompt = """
        You are a legal expert specializing in policy review. Your task is to review policies for:
        - Legal compliance and risk assessment
        - Regulatory requirements
        - Potential liabilities
        - Clarity of legal language
        - Consistency with applicable laws

        Provide detailed feedback on legal aspects, suggest improvements, and identify potential issues.
        """

    def review_policy(self, policy_text):
        """Review the policy for legal compliance and provide feedback."""
        prompt = f"""
        {self.system_prompt}

        Policy to Review:
        {policy_text}

        Please provide a comprehensive legal review including:
        1. Overall legal compliance assessment
        2. Identified legal risks or issues
        3. Regulatory compliance gaps
        4. Recommendations for legal improvements
        5. Suggested legal language clarifications

        Be specific and actionable in your feedback.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
