"""Funciones utilitarias para cargar catalogos desde `data/`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_json_relative(path: str) -> Any:
    """Lee un archivo JSON dentro de la carpeta `data`."""

    with (DATA_DIR / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_skills() -> dict[str, Any]:
    """Carga `skills_library.json`."""

    return load_json_relative("skills_library.json")


def load_courses() -> dict[str, Any]:
    """Carga `courses_db.json`."""

    return load_json_relative("courses_db.json")
