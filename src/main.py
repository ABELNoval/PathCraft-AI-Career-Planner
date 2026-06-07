"""
Punto de entrada para el planeador PathCraft.
Este archivo demuestra cómo cargar datos y ejecutar un flujo mínimo del planificador.
"""

from src.utils.data_loader import load_courses, load_skills


def main():
    skills = load_skills()
    courses = load_courses()
    print("Skills cargadas:", list(skills.get('skills', [])))
    print("Courses cargados:", list(courses.get('courses', [])))


if __name__ == '__main__':
    main()
"""Punto de entrada del planeador de carrera."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Construye la interfaz de linea de comandos del proyecto."""
    parser = argparse.ArgumentParser(description="PathCraft AI Career Planner")
    parser.add_argument("--current_skills", default="", help="Habilidades actuales separadas por comas")
    parser.add_argument("--target", default="", help="Meta profesional a alcanzar")
    return parser


def main() -> int:
    """Ejecuta el flujo principal del proyecto."""
    parser = build_parser()
    args = parser.parse_args()
    print("PathCraft listo para planear rutas de aprendizaje.")
    print(f"Habilidades actuales: {args.current_skills}")
    print(f"Objetivo: {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
