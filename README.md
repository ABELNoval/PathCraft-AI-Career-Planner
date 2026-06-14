# PathCraft: AI Career Path Planner

PathCraft is an academic Artificial Intelligence project that combines Large Language Models (LLMs), STRIPS planning, and heuristic search to generate personalized learning paths.

Given a learner's current skills and a career goal expressed in natural language, the system translates the objective into a formal planning goal, searches a catalog of courses and skills, and generates an optimal learning route based on course costs and prerequisite constraints.

The project was developed as part of an Artificial Intelligence course and demonstrates the integration of symbolic planning techniques with modern language models.

## Features

* Natural-language career goal interpretation using a local LLM.
* STRIPS-style representation of states, skills, and course actions.
* A* search for optimal learning path generation.
* Relaxed-cost admissible heuristic for cost-based planning.
* Goal translation validation.
* Route validation based on prerequisites and acquired skills.
* Support for multiple alternative learning paths.
* Fully local execution through Ollama.

## Technologies

* Python 3
* Ollama
* Gemma4:e4b
* STRIPS Planning
* A* Search
* JSON

## System Architecture

```text
User Goal
     |
     v
+-------------------+
| Gemma4:e4b (LLM)  |
| via Ollama        |
+-------------------+
     |
     v
Goal Translation
     |
     v
Goal Validation
     |
     v
STRIPS Planner
     |
     v
A* Search + Relaxed Cost Heuristic
     |
     v
Optimal Learning Route
```

## Project Structure

```text
PathCraft-AI-Career-Planner/
|-- data/                  # Skills and courses catalogs
|-- docs/                  # Technical report
|-- src/
|   |-- main.py            # CLI entry point
|   |-- planning/          # STRIPS model and search algorithms
|   |-- llm/               # LLM integration, parsing and validation
|   `-- utils/             # Data loading utilities
|-- tests/                 # Automated tests
|-- requirements.txt
`-- README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install and run Ollama:

```bash
ollama pull gemma4:e4b
ollama serve
```

## Run

From the project root:

```bash
python src/main.py --current_skills "..." --target "..."
```

## Heuristic

The planner uses a relaxed-cost admissible heuristic.

For every missing goal skill, the heuristic recursively estimates the minimum remaining cost required to obtain it by analyzing available courses and prerequisite chains.

This estimation never overestimates the true remaining cost, allowing A* to preserve optimality while exploring significantly fewer states.

## Current Career Paths

The catalog currently contains learning routes related to:

* Data Analysis
* Data Science
* Machine Learning
* Data Engineering

Each path can be reached through different combinations of courses, allowing the planner to compare alternative routes and choose the least costly solution.

## Limitations

* Recommendations are limited to the skills available in the catalog.
* Course costs are manually defined.
* The planner currently optimizes only one objective (cost).
* User preferences are not yet considered.
* The quality of recommendations depends on catalog completeness.

## Future Improvements

* Multi-objective optimization (cost, duration, difficulty).
* Larger and more realistic course catalogs.
* Personalized recommendations based on user profiles.
* Dynamic catalog generation.
* Support for additional professional domains.
