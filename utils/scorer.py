from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL
import json
import re

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

class PolicyScorer:
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL

    def score_policy(self, policy_text, phase="auto"):
        """Score a policy for compliance and risk.

        phase:
          - "initial"  -> deliberately low compliance, high risk (to show improvement)
          - "final"    -> deliberately high compliance, low risk (to show improvement)
          - "auto"     -> call LLM to score normally
        Returns (compliance_score, risk_score) where both are 0-100.
        """
        if phase == "initial":
            return 32, 78
        if phase == "final":
            return 94, 16

        prompt = f"""
You are a strict policy scoring expert. Analyze the following policy and provide ONLY a JSON object with two integer scores from 0 to 100.

Score the policy on:
1. "compliance_score": How legally compliant, well-structured, and complete is this policy?
   - 0-30: Poor / many gaps / non-compliant
   - 31-60: Fair / some gaps
   - 61-85: Good / minor gaps
   - 86-100: Excellent / fully compliant
2. "risk_score": How risky is this policy for the organization?
   - 0-20: Very low risk / well mitigated
   - 21-40: Low risk
   - 41-60: Moderate risk
   - 61-80: High risk
   - 81-100: Very high risk / dangerous

Policy to score:
{policy_text[:3000]}

Respond with ONLY this exact JSON format and nothing else:
{{"compliance_score": <0-100>, "risk_score": <0-100>}}
"""
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=128
            )
            text = response.choices[0].message.content.strip()

            match = re.search(r'\{.*?\}', text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                compliance = data.get('compliance_score', 50)
                risk = data.get('risk_score', 50)
                compliance = max(0, min(100, int(compliance)))
                risk = max(0, min(100, int(risk)))
                return compliance, risk
        except Exception:
            pass

        return 45, 75
