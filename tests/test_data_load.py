"""Tests de carga y consistencia de los catalogos locales."""

from src.utils.data_loader import load_courses, load_skills


def test_load_skills_catalog_has_realistic_entries() -> None:
    skills = load_skills()

    assert "skills" in skills
    assert len(skills["skills"]) >= 12
    assert any(skill["id"] == "skill_12" for skill in skills["skills"])
    assert "CatÃ" not in skills["description"]


def test_load_courses_catalog_has_reachable_outcomes() -> None:
    courses = load_courses()
    skill_ids = {skill["id"] for skill in load_skills()["skills"]}

    assert "courses" in courses
    assert len(courses["courses"]) >= 10
    for course in courses["courses"]:
        assert set(course["prerequisites"]).issubset(skill_ids)
        assert set(course["outcomes"]).issubset(skill_ids)
