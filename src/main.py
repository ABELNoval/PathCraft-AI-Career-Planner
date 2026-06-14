"""Punto de entrada del planeador de carrera."""

from __future__ import annotations

import argparse

from llm.client import LLMClient
from llm.goal_parser import GoalParser
from llm.validator import validate_goal_translation, validate_path
from planning.search_algo import find_path
from planning.strips_model import Action, State
from utils.data_loader import load_courses, load_skills

llm = LLMClient()
parse = GoalParser(llm)

def build_parser() -> argparse.ArgumentParser:
    """Construye la interfaz de linea de comandos del proyecto."""

    parser = argparse.ArgumentParser(description="PathCraft AI Career Planner")
    parser.add_argument("--current_skills", default="", help="Habilidades actuales separadas por comas")
    parser.add_argument("--target", default="", help="Meta profesional a alcanzar")
    return parser


def _parse_skill_list(text: str) -> list[str]:
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def _normalize_current_skills(raw_skills: list[str], skills_catalog: list[dict]) -> list[str]:
    skill_index: dict[str, str] = {}
    for skill in skills_catalog:
        skill_id = str(skill.get("id", "")).strip()
        skill_name = str(skill.get("name", "")).strip().lower()
        if skill_id:
            skill_index[skill_id.lower()] = skill_id
        if skill_name:
            skill_index[skill_name] = skill_id or skill_name

    normalized: list[str] = []
    for skill in raw_skills:
        normalized.append(skill_index.get(skill, skill))
    return normalized


def main() -> int:
    """Ejecuta el flujo basico: cargar datos, traducir meta y buscar ruta."""

    parser = build_parser()
    args = parser.parse_args()

    skills_data = load_skills()
    skills_catalog = skills_data.get("skills", [])
    courses_catalog = load_courses().get("courses", [])

    parsed_goal = parse.parse_goal(
        args.target,
        skills_data
    )

    goal_validation = validate_goal_translation(
        parsed_goal,
        skills_catalog
    )

    goal_skills = set(
        goal_validation["target_skills"]
    )

    current_skills = _normalize_current_skills(_parse_skill_list(args.current_skills), skills_catalog)
    initial_state = State.from_iterable(current_skills)
    actions = [Action.from_course_record(course) for course in courses_catalog]

    print("\n" + "=" * 60)
    print("PATHCRAFT AI CAREER PLANNER")
    print("=" * 60)

    print("\nObjetivo solicitado:")
    print(f"  {args.target}")

    if not goal_validation["valid"]:
        print("\nResultado:")
        print("  No fue posible asociar la meta a ninguna habilidad del catalogo.")
        return 0

    print("\nObjetivo interpretado:")
    for skill in goal_validation["target_skills"]:
        print(f"  - {skill}")

    path = find_path(
        initial_state,
        goal_skills,
        actions
    )

    print("\nRuta de aprendizaje recomendada:")
    print("-" * 60)

    if not path:
        print("No se encontro una ruta valida.")
        return 0

    course_costs = {
        course["title"]: course["cost"]
        for course in courses_catalog
    }

    total_cost = 0

    for index, course_name in enumerate(path, start=1):
        cost = course_costs.get(course_name, 0)
        total_cost += cost

        print(f"{index}. {course_name}")
        print(f"   Coste: {cost}")

    path_validation = validate_path(
        path,
        initial_state=initial_state,
        goal_skills=goal_skills,
        actions=actions,
        skills_catalog=skills_catalog,
    )

    print("\n" + "-" * 60)
    print("RESUMEN")
    print("-" * 60)

    print(f"Cursos requeridos : {len(path)}")
    print(f"Coste total       : {total_cost}")

    if path_validation["valid"]:
        print("Ruta valida       : SI")
    else:
        print("Ruta valida       : NO")

    print("=" * 60)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
