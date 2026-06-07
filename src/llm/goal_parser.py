"""
Traduce texto natural en metas formales (placeholder).
En producción se usaría un LLM para parsear y mapear a habilidades/cursos.
"""

def parse_goal_text(text):
    """Devuelve un dict con metas y etiquetas aproximadas.

    Por ahora es un stub que devuelve la cadena original en `raw`.
    """
    return {"raw": text, "tags": []}
"""Traduce objetivos en lenguaje natural a una meta formal."""

from __future__ import annotations


def parse_goal(text: str) -> str:
    """Convierte una descripcion libre en una meta normalizada."""
    return text.strip().lower()
