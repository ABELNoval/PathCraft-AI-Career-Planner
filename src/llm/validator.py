"""
Módulo para validar rutas con ayuda de un LLM.
Contendrá funciones que evalúan la coherencia semántica de una ruta propuesta.
"""

def validate_plan_with_llm(plan):
    """Placeholder: en un sistema real llamaría a un LLM para evaluar `plan`.
    Devuelve un dict con `score` y `notes`.
    """
    return {"score": 0.5, "notes": "Stub - integrar LLM para validaciones reales."}
"""Valida la coherencia de la ruta propuesta con apoyo de un LLM."""

from __future__ import annotations


def validate_path(path: list[str]) -> bool:
    """Marca como valida una ruta no vacia en este template inicial."""
    return bool(path)
