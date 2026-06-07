"""Punto de entrada del planeador de carrera."""

from __future__ import annotations

import argparse

from llm.goal_parser import parse_goal
from llm.validator import validate_goal_translation, validate_path
from planning.search_algo import find_path
from planning.strips_model import Action, State
from utils.data_loader import load_courses, load_skills


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

    skills_catalog = load_skills().get("skills", [])
    courses_catalog = load_courses().get("courses", [])

    parsed_goal = parse_goal(args.target, skills_catalog)
    goal_validation = validate_goal_translation(parsed_goal)

    current_skills = _normalize_current_skills(_parse_skill_list(args.current_skills), skills_catalog)
    initial_state = State.from_iterable(current_skills)
    actions = [Action.from_course_record(course) for course in courses_catalog]

    print("PathCraft listo para planear rutas de aprendizaje.")
    print(f"Meta original: {args.target}")
    print(f"Meta formal: {parsed_goal['goal_skill_id']}")
    print(f"Validacion del traductor: {goal_validation}")

    if parsed_goal["goal_skill_id"]:
        path = find_path(initial_state, parsed_goal["goal_skill_id"], actions)
        print(f"Ruta sugerida: {path}")
        print(f"Ruta valida: {validate_path(path)}")
    else:
        print("No se pudo inferir una meta formal.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
