"""
Tests mínimos para comprobar que los JSON se cargan correctamente.
Ejecutar con: `python -m pytest tests` (si pytest está instalado).
"""

from src.utils.data_loader import load_skills, load_courses


def test_load_skills():
    skills = load_skills()
    assert 'skills' in skills


def test_load_courses():
    courses = load_courses()
    assert 'courses' in courses
