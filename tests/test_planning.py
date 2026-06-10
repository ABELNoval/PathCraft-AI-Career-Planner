"""Tests del planificador A* y la validacion de rutas."""

from src.llm.validator import validate_goal_translation, validate_path
from src.planning.search_algo import find_path
from src.planning.strips_model import Action, State
from src.utils.data_loader import load_courses, load_skills


def _actions() -> list[Action]:
    return [Action.from_course_record(course) for course in load_courses()["courses"]]


def _path_cost(path: list[str], actions: list[Action]) -> float:
    action_by_name = {action.name: action for action in actions}
    return sum(action_by_name[step].cost for step in path)


def test_find_path_reaches_data_science_goal_from_scratch() -> None:
    actions = _actions()
    initial_state = State.from_iterable([])

    path = find_path(initial_state, "skill_12", actions)
    validation = validate_path(
        path,
        initial_state=initial_state,
        goal_skill="skill_12",
        actions=actions,
        skills_catalog=load_skills()["skills"],
    )

    assert path
    assert validation["valid"] is True
    assert "End-to-End Data Science Capstone" in path
    assert "Zero-to-Capstone Data Science Bootcamp" not in path


def test_find_path_prefers_lower_cost_alternative_track() -> None:
    actions = _actions()

    path = find_path(State.from_iterable([]), "skill_12", actions)

    assert "Machine Learning Intensive Track" in path
    assert "Feature Engineering Workshop" not in path
    assert "Applied Supervised Machine Learning" not in path
    assert "Unsupervised Learning for Exploration" not in path
    assert _path_cost(path, actions) == 27.0


def test_find_path_returns_empty_for_unreachable_goal() -> None:
    path = find_path(State.from_iterable([]), "skill_99", _actions())

    assert path == []


def test_validate_path_rejects_wrong_course_order() -> None:
    validation = validate_path(
        ["Applied Supervised Machine Learning"],
        initial_state=State.from_iterable([]),
        goal_skill="skill_12",
        actions=_actions(),
        skills_catalog=load_skills()["skills"],
    )

    assert validation["valid"] is False
    assert "no es aplicable" in validation["notes"]


def test_goal_validation_rejects_unknown_catalog_skill() -> None:
    validation = validate_goal_translation({"goal_skill_id": "skill_99"}, load_skills()["skills"])

    assert validation["valid"] is False
