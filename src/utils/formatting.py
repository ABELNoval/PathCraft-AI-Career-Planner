"""Formatea salidas legibles para rutas y recomendaciones."""

from __future__ import annotations

from typing import Iterable


def format_path(items: Iterable[str]) -> str:
    """Une una secuencia de pasos en una representacion amigable."""
    return " -> ".join(items)
