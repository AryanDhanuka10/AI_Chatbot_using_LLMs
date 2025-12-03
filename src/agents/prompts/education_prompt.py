"""Module: education_prompt.

Prompt template for EducationAgent using context-aware formatting.
"""

from typing import Dict

from src.agents.prompts.base_prompt import BasePromptTemplate


class EducationPrompt(BasePromptTemplate):
    """Prompt template for educational explanations."""

    def build_prompt(self, query: str, context: Dict) -> str:
        """Build a context-aware educational prompt.

        Args:
        ----
            query: The user query.
            context: Conversation memory and state.

        Returns:
        -------
            A formatted prompt string tailored for educational explanations.

        """
        memory_section = "\n".join(context.get("memory", []))

        return f"""
You are a highly skilled educational tutor specializing in clear, "
"step-by-step explanations.

Conversation History:
{memory_section}

Current Question:
{query}

Respond with:
- simple explanation first,
- deeper understanding next,
- examples where helpful,
- do not hallucinate facts.
"""
