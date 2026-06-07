"""Valida el resultado del traductor de objetivos y la ruta propuesta."""

from __future__ import annotations

from typing import Any


def validate_goal_translation(parsed_goal: dict[str, Any]) -> dict[str, Any]:
    """Da una validacion basica del objetivo formal generado."""

    goal_skill_id = str(parsed_goal.get("goal_skill_id", "")).strip()
    valid = bool(goal_skill_id)
    return {
        "valid": valid,
        "notes": "Objetivo formal encontrado." if valid else "No se pudo inferir una habilidad objetivo.",
    }


def validate_path(path: list[str]) -> bool:
    """Marca como valida una ruta no vacia en este template inicial."""

    return bool(path)


def validate_plan_with_llm(plan: Any) -> dict[str, Any]:
    """Compatibilidad con la version anterior del template."""

    is_valid = bool(plan)
    return {
        "score": 1.0 if is_valid else 0.0,
        "notes": "Plan valido para la demo base." if is_valid else "Plan vacio o no definido.",
    }
