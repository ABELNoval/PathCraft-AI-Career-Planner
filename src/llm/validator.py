"""Valida el resultado del traductor de objetivos y la ruta propuesta."""

from __future__ import annotations

from typing import Any

try:
    from planning.strips_model import Action, State
except ModuleNotFoundError:  # pragma: no cover - usado cuando se importa como paquete src.*
    from src.planning.strips_model import Action, State


def _known_skill_ids(skills_catalog: list[dict[str, Any]] | None) -> set[str]:
    return {str(skill.get("id", "")).strip() for skill in skills_catalog or [] if skill.get("id")}


def validate_goal_translation(
    parsed_goal: dict[str, Any],
    skills_catalog: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:

    target_skills = parsed_goal.get("target_skills", [])

    known_skills = _known_skill_ids(skills_catalog)

    valid = (
        len(target_skills) > 0
        and all(skill in known_skills for skill in target_skills)
    )

    if not target_skills:
        notes = "No se pudo inferir ninguna habilidad objetivo."

    elif not all(skill in known_skills for skill in target_skills):
        notes = "Algunas habilidades objetivo no existen en el catalogo."

    else:
        notes = "Objetivos formales encontrados en el catalogo."

    return {
        "valid": valid,
        "target_skills": target_skills,
        "notes": notes,
    }


def validate_path(
    path: list[str],
    *,
    initial_state: State | None = None,
    goal_skills: set[str] | None = None,
    actions: list[Action] | None = None,
    skills_catalog: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Valida una ruta aplicando cada curso sobre el estado actual."""

    if not path:
        return {
            "valid": False,
            "executed": [],
            "steps": [],
            "step_count": 0,
            "total_cost": 0.0,
            "final_skills": sorted((initial_state or State()).skills),
            "notes": "La ruta esta vacia.",
        }

    if actions is None or initial_state is None or goal_skills is None:
        return {
            "valid": bool(path),
            "executed": path,
            "steps": [],
            "step_count": len(path),
            "total_cost": None,
            "final_skills": [],
            "notes": "Validacion superficial: faltan estado inicial, meta o acciones.",
        }

    known_skills = _known_skill_ids(skills_catalog)
    invalid_skills = goal_skills.difference(known_skills)
    if known_skills and invalid_skills:
        return {
            "valid": False,
            "executed": [],
            "steps": [],
            "step_count": 0,
            "total_cost": 0.0,
            "final_skills": sorted(initial_state.skills),
            "notes": f"La meta '{sorted(invalid_skills)}' no existe en el catalogo.",
        }

    action_by_name = {action.name: action for action in actions}
    state = initial_state
    executed: list[str] = []
    step_details: list[dict[str, Any]] = []
    total_cost = 0.0

    for step in path:
        action = action_by_name.get(step)
        if action is None:
            return {
                "valid": False,
                "executed": executed,
                "steps": step_details,
                "step_count": len(executed),
                "total_cost": total_cost,
                "final_skills": sorted(state.skills),
                "notes": f"El curso '{step}' no existe en el catalogo.",
            }
        if not action.is_applicable(state):
            missing = sorted(action.preconditions.difference(state.skills))
            return {
                "valid": False,
                "executed": executed,
                "steps": step_details,
                "step_count": len(executed),
                "total_cost": total_cost,
                "final_skills": sorted(state.skills),
                "notes": f"El curso '{step}' no es aplicable. Faltan: {missing}.",
            }
        previous_skills = set(state.skills)
        state = state.apply(action)
        gained_skills = sorted(set(state.skills).difference(previous_skills))
        total_cost += action.cost
        executed.append(step)
        step_details.append(
            {
                "course": action.name,
                "cost": action.cost,
                "gained_skills": gained_skills,
                "resulting_skills": sorted(state.skills),
            }
        )

    reached_goal = goal_skills.issubset(state.skills)
    return {
        "valid": reached_goal,
        "executed": executed,
        "steps": step_details,
        "step_count": len(executed),
        "total_cost": total_cost,
        "final_skills": sorted(state.skills),
        "notes": "La ruta alcanza la meta." if reached_goal else "La ruta termina sin alcanzar la meta.",
    }


def validate_plan_with_llm(plan: Any) -> dict[str, Any]:
    """Compatibilidad con la version anterior del template.

    No invoca un LLM externo; resume si el plan contiene pasos verificables.
    """

    is_valid = bool(plan)
    return {
        "score": 1.0 if is_valid else 0.0,
        "notes": "Plan con contenido verificable." if is_valid else "Plan vacio o no definido.",
    }
