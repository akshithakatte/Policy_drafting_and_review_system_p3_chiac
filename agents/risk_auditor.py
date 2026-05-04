from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class RiskAuditor:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL
        self.system_prompt = """
        You are a risk management expert specializing in policy audit. Your task is to identify and assess risks in policies, including:
        - Operational risks
        - Financial risks
        - Reputational risks
        - Compliance risks
        - Strategic risks

        Provide detailed risk assessments and mitigation strategies.
        """

    def audit_policy(self, policy_text):
        """Audit the policy for risks and provide mitigation recommendations."""
        prompt = f"""
        {self.system_prompt}

        Policy to Audit:
        {policy_text}

        Please provide a comprehensive risk audit including:
        1. Identification of potential risks
        2. Risk severity assessment (High/Medium/Low)
        3. Impact analysis
        4. Mitigation strategies and recommendations
        5. Monitoring and control measures

        Be specific and provide actionable recommendations.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
