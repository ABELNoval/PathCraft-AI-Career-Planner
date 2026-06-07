"""Algoritmos de busqueda para explorar el espacio de estados del planificador."""

from __future__ import annotations

import heapq
import itertools
from typing import Callable, Iterable, Iterator, List, Optional, Sequence, Tuple

from .strips_model import Action, State

Neighbor = Tuple[State, int, Action]


def successor_states(state: State, actions: Iterable[Action]) -> Iterator[Neighbor]:
    """Genera el espacio sucesor aplicando todas las acciones validas.

    Cada sucesor representa el estado alcanzado tras completar un curso.
    El coste de cada transicion es 1 porque, por ahora, todos los cursos valen lo mismo.
    """

    for action in actions:
        if action.is_applicable(state):
            yield state.apply(action), 1, action


def astar(
    start: State,
    goal_test: Callable[[State], bool],
    neighbors_fn: Callable[[State], Iterable[Neighbor]],
    heuristic_fn: Callable[[State], int] = lambda state: 0,
) -> List[Tuple[State, Optional[Action]]]:
    """Ejecuta A* y devuelve la ruta como lista de estados y acciones."""

    counter = itertools.count()
    open_heap = [(heuristic_fn(start), 0, next(counter), start)]
    came_from: dict[State, Tuple[Optional[State], Optional[Action]]] = {start: (None, None)}
    g_score = {start: 0}

    while open_heap:
        _, current_g, _, current = heapq.heappop(open_heap)
        if goal_test(current):
            return _reconstruct_path(came_from, current)

        if current_g > g_score.get(current, float("inf")):
            continue

        for neighbor, step_cost, action in neighbors_fn(current):
            tentative_g = current_g + step_cost
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = (current, action)
                f_score = tentative_g + heuristic_fn(neighbor)
                heapq.heappush(open_heap, (f_score, tentative_g, next(counter), neighbor))

    return []


def find_path(initial_state: State, goal_skill: str, actions: Iterable[Action]) -> List[str]:
    """Busca una secuencia de cursos que consiga la habilidad objetivo."""

    route = astar(
        start=initial_state,
        goal_test=lambda state: goal_skill in state.skills,
        neighbors_fn=lambda state: successor_states(state, actions),
    )
    return [action.name for _, action in route if action is not None]


def _reconstruct_path(
    came_from: dict[State, Tuple[Optional[State], Optional[Action]]],
    current: State,
) -> List[Tuple[State, Optional[Action]]]:
    path: List[Tuple[State, Optional[Action]]] = []
    while True:
        previous_state, action = came_from[current]
        path.append((current, action))
        if previous_state is None:
            break
        current = previous_state
    path.reverse()
    return path
