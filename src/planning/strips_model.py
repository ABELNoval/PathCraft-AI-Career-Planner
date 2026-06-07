"""
Definición de modelos STRIPS simplificados: estados y acciones.
Contiene clases y comentarios para guiar la implementación.
"""

class State:
    """Representa un estado como un conjunto de hechos."""
    def __init__(self, facts=None):
        self.facts = set(facts or [])

    def satisfies(self, goal_facts):
        return set(goal_facts).issubset(self.facts)


class Action:
    """Acción con precondiciones y efectos (add/delete)."""
    def __init__(self, name, preconditions=None, add_effects=None, del_effects=None):
        self.name = name
        self.preconditions = set(preconditions or [])
        self.add_effects = set(add_effects or [])
        self.del_effects = set(del_effects or [])
"""Definicion del modelo STRIPS usado para representar estados y acciones."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Iterable


@dataclass(frozen=True)
class Action:
    """Accion aplicable sobre un estado de habilidades."""

    name: str
    preconditions: FrozenSet[str] = field(default_factory=frozenset)
    effects: FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class State:
    """Estado formal del sistema de habilidades del estudiante."""

    skills: FrozenSet[str] = field(default_factory=frozenset)

    @classmethod
    def from_iterable(cls, skills: Iterable[str]) -> "State":
        return cls(skills=frozenset(skills))
