"""
Algoritmos de búsqueda (A*): implementación mínima y explicativa.
"""

import heapq


def astar(start, goal_test, neighbors_fn, heuristic_fn=lambda s: 0):
    """Ejemplo simple de A* que opera sobre estados abstractos.

    - `start`: estado inicial
    - `goal_test(state)`: devuelve True si `state` satisface el objetivo
    - `neighbors_fn(state)`: devuelve iterable de (neighbor_state, cost, action)
    - `heuristic_fn(state)`: coste heurístico estimado hasta objetivo
    """
    open_heap = [(heuristic_fn(start), 0, start, None)]
    came_from = {}
    g_score = {start: 0}

    while open_heap:
        _, g, current, action = heapq.heappop(open_heap)
        if goal_test(current):
            return current
        for neighbor, step_cost, act in neighbors_fn(current):
            tentative_g = g + step_cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic_fn(neighbor)
                heapq.heappush(open_heap, (f, tentative_g, neighbor, act))
                came_from[neighbor] = (current, act)
    return None
"""Algoritmo de busqueda para encontrar rutas de aprendizaje."""

from __future__ import annotations

from typing import Iterable, List

from .strips_model import Action, State


def find_path(initial_state: State, goal_skill: str, actions: Iterable[Action]) -> List[str]:
    """Devuelve una ruta simple placeholder hacia la meta."""
    _ = initial_state
    _ = goal_skill
    return [action.name for action in actions]
