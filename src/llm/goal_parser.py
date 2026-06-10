"""Traduce objetivos en lenguaje natural a habilidades meta formales."""

from __future__ import annotations

import re
from typing import Any, Sequence, cast

SkillRecord = dict[str, Any]
CatalogData = dict[str, Any]
SkillCatalogInput = Sequence[SkillRecord] | CatalogData | None


def _build_skill_index(skills_catalog: Sequence[SkillRecord]) -> dict[str, str]:
    index: dict[str, str] = {}
    for skill in skills_catalog:
        skill_id = str(skill.get("id", "")).strip()
        skill_name = str(skill.get("name", "")).strip().lower()
        if skill_id:
            index[skill_id.lower()] = skill_id
        if skill_name:
            index[skill_name] = skill_id or skill_name
        for alias in skill.get("aliases", []):
            alias_text = str(alias).strip().lower()
            if alias_text:
                index[alias_text] = skill_id or alias_text
    return index


def _build_role_index(catalog: dict[str, Any] | None) -> dict[str, str]:
    index: dict[str, str] = {}
    if not catalog:
        return index

    for role in catalog.get("target_roles", []):
        goal_skill_id = str(role.get("goal_skill_id", "")).strip()
        if not goal_skill_id:
            continue
        role_name = str(role.get("name", "")).strip().lower()
        role_id = str(role.get("id", "")).strip().lower()
        if role_name:
            index[role_name] = goal_skill_id
        if role_id:
            index[role_id] = goal_skill_id
        for alias in role.get("aliases", []):
            alias_text = str(alias).strip().lower()
            if alias_text:
                index[alias_text] = goal_skill_id
    return index


def _extract_catalog_parts(
    skills_catalog: SkillCatalogInput,
) -> tuple[list[SkillRecord], CatalogData | None]:
    if skills_catalog is None:
        return [], None
    if isinstance(skills_catalog, dict):
        raw_skills: object = skills_catalog.get("skills")
        skills = raw_skills if isinstance(raw_skills, list) else []
        skill_records = [cast(SkillRecord, skill) for skill in skills if isinstance(skill, dict)]
        return skill_records, skills_catalog
    return list(skills_catalog), None


def parse_goal(
    text: str,
    skills_catalog: SkillCatalogInput = None,
) -> dict[str, Any]:
    """Convierte una meta libre en una meta formal simple.

    Este parser ocupa el rol de traduccion de lenguaje natural sin depender
    de una API externa: normaliza el texto y lo mapea a habilidades/roles
    declarados en el catalogo local.
    """

    raw_text = text.strip()
    normalized_text = re.sub(r"\s+", " ", raw_text).lower()
    skills, catalog = _extract_catalog_parts(skills_catalog)
    skill_index = _build_skill_index(skills)
    role_index = _build_role_index(catalog)
    matched_skill_ids: list[str] = []

    explicit_ids = re.findall(r"skill_\d+", normalized_text)
    matched_skill_ids.extend(explicit_ids)

    numbered_skill = re.findall(r"habilidad\s+(\d+)", normalized_text)
    matched_skill_ids.extend([f"skill_{int(number):02d}" for number in numbered_skill])

    for role_name, mapped_id in role_index.items():
        if role_name and role_name in normalized_text:
            matched_skill_ids.append(mapped_id)

    for skill_name, mapped_id in skill_index.items():
        if skill_name and skill_name in normalized_text:
            matched_skill_ids.append(mapped_id)

    deduplicated_matches = list(dict.fromkeys(matched_skill_ids))
    goal_skill_id = deduplicated_matches[0] if deduplicated_matches else ""

    return {
        "raw_text": raw_text,
        "normalized_text": normalized_text,
        "goal_skill_id": goal_skill_id,
        "matched_skill_ids": deduplicated_matches,
        "confidence": 1.0 if deduplicated_matches else 0.0,
    }
