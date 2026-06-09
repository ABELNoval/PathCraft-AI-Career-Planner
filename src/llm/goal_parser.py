"""Traduce objetivos en lenguaje natural a habilidades meta formales."""

from __future__ import annotations

import re
from typing import Any, Iterable


def _build_skill_index(skills_catalog: Iterable[dict[str, Any]]) -> dict[str, str]:
    index: dict[str, str] = {}
    for skill in skills_catalog:
        skill_id = str(skill.get("id", "")).strip()
        skill_name = str(skill.get("name", "")).strip().lower()
        if skill_id:
            index[skill_id.lower()] = skill_id
        if skill_name:
            index[skill_name] = skill_id or skill_name
    return index


def parse_goal(
    text: str, skills_catalog: Iterable[dict[str, Any]] | None = None
) -> dict[str, Any]:
    """Convierte una meta libre en una meta formal simple.

    Este parser es un paso base del rol del LLM: normaliza el texto y trata
    de mapearlo a una habilidad existente del catalogo.
    """

    raw_text = text.strip()
    normalized_text = re.sub(r"\s+", " ", raw_text).lower()
    skill_index = _build_skill_index(skills_catalog or [])
    matched_skill_ids: list[str] = []

    explicit_ids = re.findall(r"skill_\d+", normalized_text)
    matched_skill_ids.extend(explicit_ids)

    numbered_skill = re.findall(r"habilidad\s+(\d+)", normalized_text)
    matched_skill_ids.extend([f"skill_{int(number):02d}" for number in numbered_skill])

    for skill_name, mapped_id in skill_index.items():
        if skill_name and skill_name in normalized_text:
            matched_skill_ids.append(mapped_id)

    deduplicated_matches = list(dict.fromkeys(matched_skill_ids))
    goal_skill_id = deduplicated_matches[0] if deduplicated_matches else normalized_text

    return {
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "goal_skill_id": goal_skill_id,
        "matched_skill_ids": deduplicated_matches,
        "confidence": 1.0 if deduplicated_matches else 0.25,
    }
