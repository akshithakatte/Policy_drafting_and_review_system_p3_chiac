from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class PolicyDrafter:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL
        self.system_prompt = """
        You are a policy drafting expert. Your task is to create comprehensive, well-structured policies
        that are clear, concise, and compliant with general best practices. Focus on:
        - Clear objectives and scope
        - Defined roles and responsibilities
        - Implementation guidelines
        - Compliance requirements
        - Monitoring and review processes
        """

    def draft_policy(self, topic, requirements=None):
        """Draft an initial policy based on the topic and requirements."""
        prompt = f"""
        {self.system_prompt}

        Topic: {topic}
        Additional Requirements: {requirements or "None specified"}

        Please draft a comprehensive policy document. Structure it with:
        1. Title
        2. Purpose
        3. Scope
        4. Policy Statements
        5. Procedures
        6. Roles and Responsibilities
        7. Compliance and Enforcement
        8. Review and Updates

        Make it professional, detailed, and practical.
        """

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content.strip()
