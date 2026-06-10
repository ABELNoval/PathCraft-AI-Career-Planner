"""Algoritmos de busqueda para explorar el espacio de estados del planificador."""

from __future__ import annotations

import heapq
import itertools
from typing import Callable, Iterable, Iterator, List, Optional, Set, Tuple

from .strips_model import Action, State

Neighbor = Tuple[State, float, Action]


def build_missing_skills_heuristic(goal_skills: Iterable[str]) -> Callable[[State], float]:
    """Construye una heuristica admisible que cuenta habilidades objetivo faltantes.

    Si el objetivo es un conjunto de habilidades, esta estimacion nunca supera
    el coste real minimo cuando cada curso tiene coste unitario.
    """

    goal_set: Set[str] = set(goal_skills)

    def heuristic(state: State) -> float:
        return float(len(goal_set.difference(state.skills)))

    return heuristic


def goal_skill_heuristic(goal_skill: str) -> Callable[[State], float]:
    """Heuristica conveniencia para una unica habilidad meta."""

    return build_missing_skills_heuristic([goal_skill])


def build_relaxed_cost_heuristic(goal_skill: str, actions: Iterable[Action]) -> Callable[[State], float]:
    """Estima un coste restante conservador usando prerequisitos relajados.

    Para una habilidad faltante, estima el coste del curso mas barato que la
    produce mas el prerequisito individual mas caro que aun falte. Usar el maximo
    evita sumar prerequisitos compartidos dos veces y mantiene la estimacion por
    debajo del coste real en catalogos de aprendizaje sin efectos de borrado.
    """

    producers_by_skill: dict[str, list[Action]] = {}
    for action in actions:
        for skill in action.add_effects:
            producers_by_skill.setdefault(skill, []).append(action)

    def estimate_skill_cost(skill: str, known_skills: Set[str], visiting: Set[str]) -> float:
        if skill in known_skills:
            return 0.0
        if skill in visiting:
            return float("inf")

        best_cost = float("inf")
        for action in producers_by_skill.get(skill, []):
            prereq_costs = [
                estimate_skill_cost(prereq, known_skills, visiting | {skill})
                for prereq in action.preconditions
                if prereq not in known_skills
            ]
            if any(cost == float("inf") for cost in prereq_costs):
                continue
            prereq_lower_bound = max(prereq_costs, default=0.0)
            best_cost = min(best_cost, action.cost + prereq_lower_bound)
        return best_cost

    def heuristic(state: State) -> float:
        estimate = estimate_skill_cost(goal_skill, set(state.skills), set())
        return 0.0 if estimate == float("inf") else estimate

    return heuristic


def successor_states(state: State, actions: Iterable[Action]) -> Iterator[Neighbor]:
    """Genera el espacio sucesor aplicando todas las acciones validas.

    Cada sucesor representa el estado alcanzado tras completar un curso.
    El coste de la transicion se toma del coste propio de cada accion/curso.
    """

    for action in actions:
        if action.is_applicable(state):
            yield state.apply(action), action.cost, action


def astar(
    start: State,
    goal_test: Callable[[State], bool],
    neighbors_fn: Callable[[State], Iterable[Neighbor]],
    heuristic_fn: Callable[[State], float] = lambda state: 0.0,
) -> List[Tuple[State, Optional[Action]]]:
    """Ejecuta A* y devuelve la ruta como lista de estados y acciones."""

    counter = itertools.count()
    open_heap = [(heuristic_fn(start), 0.0, next(counter), start)]
    came_from: dict[State, Tuple[Optional[State], Optional[Action]]] = {start: (None, None)}
    g_score: dict[State, float] = {start: 0.0}

    while open_heap:
        _, current_g, _, current = heapq.heappop(open_heap)
        if goal_test(current):
            return _reconstruct_path(came_from, current)

        if current_g > g_score.get(current, float("inf")):
            continue

        for neighbor, step_cost, action in neighbors_fn(current):
            tentative_g = float(current_g) + float(step_cost)
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = float(tentative_g)
                came_from[neighbor] = (current, action)
                f_score = tentative_g + float(heuristic_fn(neighbor))
                heapq.heappush(open_heap, (f_score, tentative_g, next(counter), neighbor))

    return []


def find_path(initial_state: State, goal_skill: str, actions: Iterable[Action]) -> List[str]:
    """Busca una secuencia de cursos que consiga la habilidad objetivo."""

    action_list = list(actions)
    heuristic_fn = build_relaxed_cost_heuristic(goal_skill, action_list)
    route = astar(
        start=initial_state,
        goal_test=lambda state: goal_skill in state.skills,
        neighbors_fn=lambda state: successor_states(state, action_list),
        heuristic_fn=heuristic_fn,
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
