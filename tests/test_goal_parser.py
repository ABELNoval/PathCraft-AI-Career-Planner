from src.llm.client import LLMClient
from src.llm.goal_parser import GoalParser
from src.utils.data_loader import load_skills

llm = LLMClient()
parser = GoalParser(llm)

result = parser.parse_goal(
    "Quiero aprender machine learning",
    load_skills()
)

print(result)
