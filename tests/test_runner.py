from src.llm.client import LLMClient
from src.llm.goal_parser import GoalParser
from src.llm.validator import validate_goal_translation, validate_path
from src.planning.search_algo import find_path
from src.planning.strips_model import Action, State
from src.utils.data_loader import load_courses, load_skills


def _normalize_current_skills(skills):
    return set(skills)


def run_case(name, goal_text, current_skills):
    print("\n" + "=" * 60)
    print(f"CASE: {name}")
    print("=" * 60)

    skills_data = load_skills()
    skills_catalog = skills_data["skills"]
    courses_catalog = load_courses()["courses"]

    llm = LLMClient()
    parser = GoalParser(llm)

    parsed_goal = parser.parse_goal(goal_text, skills_data)

    validation = validate_goal_translation(parsed_goal, skills_catalog)

    print("Goal text:", goal_text)
    print("Parsed skills:", parsed_goal["target_skills"])
    print("Validation:", validation)

    if not validation["valid"]:
        print("INVALID GOAL -> skipped")
        return

    goal_skills = set(parsed_goal["target_skills"])

    initial_state = State.from_iterable(_normalize_current_skills(current_skills))
    actions = [Action.from_course_record(c) for c in courses_catalog]

    path = find_path(initial_state, goal_skills, actions)

    print("Path:", path)

    path_validation = validate_path(
        path,
        initial_state=initial_state,
        goal_skills=goal_skills,
        actions=actions,
        skills_catalog=skills_catalog,
    )

    print("Validation result:", path_validation)


def main():

    # -------------------------
    # CASE 1: ML / Data Science
    # -------------------------
    run_case(
        "Machine Learning Goal (base case)",
        "I want to learn machine learning",
        current_skills=["skill_01"]
    )

    # -------------------------
    # CASE 2: Data Engineer optimal path
    # -------------------------
    run_case(
        "Data Engineer optimal path",
        "I want to become a Data Engineer",
        current_skills=[]
    )

    # -------------------------
    # CASE 3: Cost inversion test (bootcamp vs normal path)
    # -------------------------
    run_case(
        "Cost sensitivity test (bootcamp dominance)",
        "I want to become a Data Scientist",
        current_skills=[]
    )

    # -------------------------
    # CASE 4: Invalid / out of domain goal
    # -------------------------
    run_case(
        "Invalid goal (out of domain)",
        "I want to become an astronaut",
        current_skills=[]
    )


if __name__ == "__main__":
    main()
