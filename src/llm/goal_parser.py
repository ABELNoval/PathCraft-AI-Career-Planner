import json
from typing import Any
from urllib import response

from llm.client import LLMClient


class GoalParser:

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def parse_goal(
        self,
        goal_text: str,
        available_skills: dict[str, Any]
    ) -> dict:

        prompt = f"""
You are a career planning assistant.

Your task is to translate a user's professional goal into the final skills that best represent that goal.

IMPORTANT:

You are NOT a planner.

You are NOT responsible for finding prerequisite skills.

You are NOT responsible for building a learning path.

A separate STRIPS planner and A* search algorithm will discover prerequisites and learning sequences later.

Your job is ONLY to identify the final target skills requested or implied by the user's goal.

IMPORTANT RULES:

1. Use ONLY skills that exist in the provided catalog.
2. Never invent skill IDs.
3. Never invent skills.
4. Do NOT include prerequisite skills.
5. Do NOT include intermediate skills.
6. Return ONLY the final target skills that represent the user's objective.
7. If a skill depends on other skills, return ONLY that skill.
8. The planner will discover dependencies later.
9. If the user asks for multiple goals, return multiple skills.
10. If no skill reasonably matches the user's goal, return an empty list.
11. Return ONLY valid JSON.
12. Do NOT explain your reasoning.
13. Do NOT include comments.
14. Do NOT include markdown.
15. Do NOT wrap the response in ```json blocks.
16. The first character of your response must be '{{'.
17. The last character of your response must be '}}'.

Examples:

User:
"I want to learn machine learning"

Output:
{{
    "target_skills": ["skill_10"]
}}

User:
"I want to learn clustering"

Output:
{{
    "target_skills": ["skill_11"]
}}

User:
"I want to learn data visualization"

Output:
{{
    "target_skills": ["skill_04"]
}}

User:
"I want to become a Data Scientist"

Output:
{{
    "target_skills": ["skill_13"]
}}

User:
"I want to become a Machine Learning Engineer"

Output:
{{
    "target_skills": ["skill_17"]
}}

User:
"I want to become a Data Engineer"

Output:
{{
    "target_skills": ["skill_21"]
}}

User:
"I want to learn machine learning and deployment"

Output:
{{
    "target_skills": ["skill_10", "skill_15"]
}}

User:
"I want to become an astronaut"

Output:
{{
    "target_skills": []
}}

IMPORTANT:

If the user asks for "Machine Learning", return ONLY:

{{
    "target_skills": ["skill_10"]
}}

Do NOT return:

{{
    "target_skills": [
        "skill_01",
        "skill_08",
        "skill_09",
        "skill_10"
    ]
}}

The planner will discover prerequisites later.

Output format:

{{
    "target_skills": [
        "skill_xx"
    ]
}}

Available catalog:
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

            for skill_id in result["target_skills"]:
                if not isinstance(skill_id, str):
                    raise ValueError(
                        "All target_skills entries must be strings."
                    )

            return result

        except json.JSONDecodeError as e:

            raise RuntimeError(
                f"Invalid JSON returned by LLM: {e}"
            )
