"""Definicion del modelo STRIPS usado para representar habilidades y cursos."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Iterable, Mapping


@dataclass(frozen=True)
class State:
    """Estado del profesional representado como un conjunto inmutable de habilidades."""

    skills: FrozenSet[str] = field(default_factory=frozenset)

    @classmethod
    def from_iterable(cls, skills: Iterable[str]) -> "State":
        return cls(skills=frozenset(skills))

    def satisfies(self, goal_skills: Iterable[str]) -> bool:
        """Comprueba si el estado contiene todas las habilidades objetivo."""
        return set(goal_skills).issubset(self.skills)

    def apply(self, action: "Action") -> "State":
        """Devuelve el nuevo estado tras ejecutar una accion valida."""
        if not action.is_applicable(self):
            raise ValueError(f"Action '{action.name}' is not applicable to this state.")
        updated_skills = set(self.skills)
        updated_skills.difference_update(action.del_effects)
        updated_skills.update(action.add_effects)
        return State.from_iterable(updated_skills)


@dataclass(frozen=True)
class Action:
    """Operador STRIPS: precondiciones, efectos de adicion y de borrado."""

    name: str
    preconditions: FrozenSet[str] = field(default_factory=frozenset)
    add_effects: FrozenSet[str] = field(default_factory=frozenset)
    del_effects: FrozenSet[str] = field(default_factory=frozenset)

    @classmethod
    def from_course_record(cls, course: Mapping[str, object]) -> "Action":
        """Construye una accion a partir de un registro de curso del catalogo."""
        return cls(
            name=str(course["title"]),
            preconditions=frozenset(course.get("prerequisites", [])),
            add_effects=frozenset(course.get("outcomes", [])),
            del_effects=frozenset(),
        )

    def is_applicable(self, state: State) -> bool:
        """Indica si el estado cumple las precondiciones de la accion."""
        return self.preconditions.issubset(state.skills)
