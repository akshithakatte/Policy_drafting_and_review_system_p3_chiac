"""
Responsibilities of this agent:
- Receive a policy topic + optional requirements
- Generate a well-structured, professional first-draft policy document
- Format the output with standard sections (Purpose, Scope, Definitions, etc.)
- Support iteration: accept prior feedback to produce an improved draft
"""

from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL


class PolicyDrafter:
    """
    Writer Agent: Generates structured policy drafts using an LLM.

    This is the first agent in the multi-agent pipeline. Its output feeds
    directly into the LegalReviewer and RiskAuditor agents.
    """

    # Standard sections every policy should include
    POLICY_SECTIONS = [
        "1. Purpose",
        "2. Scope",
        "3. Definitions",
        "4. Policy Statement",
        "5. Roles and Responsibilities",
        "6. Procedures and Guidelines",
        "7. Compliance and Enforcement",
        "8. Review and Updates",
        "9. References",
    ]

    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
        )
        self.model = LLM_MODEL

    # ------------------------------------------------------------------ #
    #  Public Methods                                                      #
    # ------------------------------------------------------------------ #

    def draft_policy(self, topic: str, requirements: str = None) -> str:
        """
        Generate an initial policy draft.

        Args:
            topic:        The subject of the policy (e.g. "Data Privacy Policy").
            requirements: Optional free-text constraints or must-have clauses.

        Returns:
            A complete policy document as a formatted string.
        """
        prompt = self._build_draft_prompt(topic, requirements)
        return self._call_llm(prompt, context="initial draft")

    def redraft_with_feedback(
        self,
        topic: str,
        previous_draft: str,
        legal_feedback: str = None,
        risk_feedback: str = None,
        requirements: str = None,
    ) -> str:
        """
        Produce an improved draft incorporating reviewer feedback.

        This method is used when the Reviser delegates back to the Writer Agent
        for a structural rewrite (as opposed to minor edits).

        Args:
            topic:           Original policy topic.
            previous_draft:  The draft that was reviewed.
            legal_feedback:  Comments from the LegalReviewer agent.
            risk_feedback:   Comments from the RiskAuditor agent.
            requirements:    Any original requirements that must still be met.

        Returns:
            Revised policy draft as a formatted string.
        """
        prompt = self._build_redraft_prompt(
            topic, previous_draft, legal_feedback, risk_feedback, requirements
        )
        return self._call_llm(prompt, context="redraft with feedback")

    def draft_section(self, topic: str, section_name: str, context: str = None) -> str:
        """
        Draft a single named section of a policy.

        Useful when only one section needs regeneration after targeted feedback.

        Args:
            topic:        The parent policy topic.
            section_name: E.g. "Roles and Responsibilities".
            context:      Other sections already written, for consistency.

        Returns:
            The drafted section as a string.
        """
        prompt = self._build_section_prompt(topic, section_name, context)
        return self._call_llm(prompt, context=f"section: {section_name}")

    # ------------------------------------------------------------------ #
    #  Prompt Builders                                                     #
    # ------------------------------------------------------------------ #

    def _build_draft_prompt(self, topic: str, requirements: str = None) -> str:
        sections_list = "\n".join(f"  {s}" for s in self.POLICY_SECTIONS)

        req_block = ""
        if requirements:
            req_block = f"""
SPECIFIC REQUIREMENTS TO INCORPORATE:
{requirements.strip()}
"""

        return f"""You are a professional Policy Writer Agent. Your task is to generate a complete, \
well-structured policy document for the given topic.

TOPIC: {topic}
{req_block}
REQUIRED SECTIONS (include ALL of these in your output):
{sections_list}

FORMATTING RULES:
- Start with a policy header block containing: Policy Title, Effective Date, Version, Owner Department
- Use the exact section numbers and names listed above as bold headers
- Write in clear, formal language appropriate for an organizational policy
- Each section should be substantive — minimum 2-3 paragraphs or a list of 4+ items
- Use numbered sub-sections where appropriate (e.g., 4.1, 4.2)
- End with a signature/approval block placeholder

OUTPUT: Produce ONLY the policy document. No meta-commentary, no preamble.
"""

    def _build_redraft_prompt(
        self,
        topic: str,
        previous_draft: str,
        legal_feedback: str = None,
        risk_feedback: str = None,
        requirements: str = None,
    ) -> str:
        sections_list = "\n".join(f"  {s}" for s in self.POLICY_SECTIONS)

        legal_block = ""
        if legal_feedback:
            legal_block = f"""
LEGAL REVIEWER FEEDBACK (must address every point):
{legal_feedback.strip()}
"""

        risk_block = ""
        if risk_feedback:
            risk_block = f"""
RISK AUDITOR FEEDBACK (must address every point):
{risk_feedback.strip()}
"""

        req_block = ""
        if requirements:
            req_block = f"""
ORIGINAL REQUIREMENTS (still apply):
{requirements.strip()}
"""

        return f"""You are a professional Policy Writer Agent performing a revision pass.

TOPIC: {topic}
{req_block}
PREVIOUS DRAFT:
{previous_draft}
{legal_block}
{risk_block}
TASK:
Rewrite the full policy document incorporating ALL feedback above. Do not skip sections. \
Improve clarity, completeness, and compliance where issues were flagged.

REQUIRED SECTIONS (all must be present in the output):
{sections_list}

IMPORTANT:
- Clearly resolve every point raised in legal and risk feedback
- Do not remove existing correct content; add/update what is needed
- Maintain formal policy language throughout
- Keep the policy header block updated (bump the version number)

OUTPUT: Produce ONLY the revised policy document.
"""

    def _build_section_prompt(
        self, topic: str, section_name: str, context: str = None
    ) -> str:
        ctx_block = ""
        if context:
            ctx_block = f"""
CONTEXT (other sections already written — maintain consistency):
{context[:1500]}
...
"""

        return f"""You are a professional Policy Writer Agent drafting a single section.

POLICY TOPIC: {topic}
SECTION TO WRITE: {section_name}
{ctx_block}
Write ONLY the content for "{section_name}". Use formal policy language. \
Include numbered sub-points where appropriate. Be thorough and specific.

OUTPUT: Produce ONLY the section content (including the bold section header).
"""

    # ------------------------------------------------------------------ #
    #  LLM Helper                                                          #
    # ------------------------------------------------------------------ #

    def _call_llm(self, prompt: str, context: str = "") -> str:
        """
        Send a prompt to the configured Groq LLM and return the response text.

        Args:
            prompt:  The full prompt string.
            context: Short description used only in error messages.

        Returns:
            The model's response as a plain string.

        Raises:
            RuntimeError: If the API call fails after retries.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior policy writer at a professional organization. "
                            "You produce complete, well-structured policy documents. "
                            "You always follow the exact output format requested."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,   # Lower = more consistent, formal output
                max_tokens=4096,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(
                f"PolicyDrafter LLM call failed (context: {context}): {e}"
            ) from e
