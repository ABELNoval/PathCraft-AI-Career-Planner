import json

from src.llm.client import LLMClient


class GoalParser:

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def parse_goal(
        self,
        goal_text: str,
        available_skills: list[str]
    ) -> dict:

        prompt = f"""
You are a career planning assistant.

Your task is to map a user's professional goal to skills.

IMPORTANT RULES:

1. Use ONLY skills from the provided list.
2. Never invent skills.
3. Never explain your reasoning.
4. Return ONLY valid JSON.
5. The JSON must have exactly this structure:

{{
    "target_role": "...",
    "target_skills": [...]
}}

Available skills:
{json.dumps(available_skills, indent=2)}

User goal:
{goal_text}
"""

        response = self.llm.generate(
            prompt=prompt,
            temperature=0.0
        )

        try:

            result = json.loads(response)

            if "target_skills" not in result:
                raise ValueError(
                    "Missing 'target_skills' field."
                )

            if not isinstance(
                result["target_skills"],
                list
            ):
                raise ValueError(
                    "'target_skills' must be a list."
                )

            return result

        except json.JSONDecodeError as e:

            raise RuntimeError(
                f"Invalid JSON returned by LLM: {e}"
            )
