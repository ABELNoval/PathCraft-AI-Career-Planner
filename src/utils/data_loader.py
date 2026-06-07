"""
Funciones utilitarias para cargar JSON de datos (`data/`).
Incluye comentarios que explican su propósito.
"""

import json
from pathlib import Path


def load_json_relative(path):
    base = Path(__file__).resolve().parents[2]
    p = base / 'data' / path
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_skills():
    """Carga `skills_library.json` y devuelve su contenido como dict."""
    return load_json_relative('skills_library.json')


def load_courses():
    """Carga `courses_db.json` y devuelve su contenido como dict."""
    return load_json_relative('courses_db.json')
"""Carga los catalogos de habilidades y cursos desde disco."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Lee un archivo JSON del proyecto."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)
