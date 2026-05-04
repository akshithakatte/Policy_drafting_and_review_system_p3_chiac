from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class Reviser:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL
        self.system_prompt = """
        You are a policy revision expert. Your task is to incorporate feedback from legal reviews and risk audits
        to improve and refine policies. Focus on:
        - Integrating legal recommendations
        - Addressing risk mitigation strategies
        - Improving clarity and readability
        - Ensuring consistency and coherence
        - Enhancing practicality and implementation
        """

    def revise_policy(self, original_policy, legal_feedback, risk_feedback):
        """Revise the policy based on feedback from legal and risk reviews."""
        prompt = f"""
        {self.system_prompt}

        Original Policy:
        {original_policy}

        Legal Review Feedback:
        {legal_feedback}

        Risk Audit Feedback:
        {risk_feedback}

        Please revise the policy by incorporating the feedback. Focus on:
        1. Addressing legal compliance issues
        2. Implementing risk mitigation measures
        3. Improving clarity and structure
        4. Ensuring the policy is practical and implementable

        Provide the revised policy with clear indications of major changes made.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content.strip()
