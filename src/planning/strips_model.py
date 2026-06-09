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
    cost: float = 1.0

    @classmethod
    def from_course_record(cls, course: Mapping[str, object]) -> "Action":
        """Construye una accion a partir de un registro de curso del catalogo."""
        # Safe parse for cost: accept int/float/str, fallback to 1.0
        raw_cost = course.get("cost", 1.0)
        parsed_cost = 1.0
        if isinstance(raw_cost, (int, float)):
            parsed_cost = float(raw_cost)
        elif isinstance(raw_cost, str):
            try:
                parsed_cost = float(raw_cost.strip())
            except ValueError:
                parsed_cost = 1.0
        # normalize negative values
        if parsed_cost < 0:
            parsed_cost = 0.0

        # Safe parse for prerequisites/outcomes: coerce to list of strings
        from collections.abc import Iterable as _Iterable

        def _coerce_list_of_str(value: object) -> list[str]:
            if value is None:
                return []
            # Strings are iterable but we want them as single elements
            if isinstance(value, (str, bytes)):
                return [str(value)]
            # dict -> use its values
            if isinstance(value, dict):
                return [str(x) for x in value.values()]
            # Lists/tuples/sets or other iterables
            if isinstance(value, (list, tuple, set)):
                return [str(x) for x in value]
            if isinstance(value, _Iterable):
                try:
                    return [str(x) for x in value]
                except Exception:
                    return []
            return []

        preconds = _coerce_list_of_str(course.get("prerequisites", []))
        outcomes = _coerce_list_of_str(course.get("outcomes", []))

        return cls(
            name=str(course.get("title", "")),
            preconditions=frozenset(preconds),
            add_effects=frozenset(outcomes),
            del_effects=frozenset(),
            cost=parsed_cost,
        )

    def is_applicable(self, state: State) -> bool:
        """Indica si el estado cumple las precondiciones de la accion."""
        return self.preconditions.issubset(state.skills)
