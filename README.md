# PathCraft: AI Career Path Planner

PathCraft is an academic AI project that combines classical planning with a lightweight natural-language goal translator. Given a learner's current skills and a career target, it searches a course catalog and proposes a valid learning route.

The current catalog models a semirealistic path toward a **Data Scientist Junior** profile.

## Features

- STRIPS-style representation of learner states and course actions.
- A* search over the skill graph.
- Local heuristic goal parser for skill names, skill IDs, aliases, and the Data Scientist target role.
- Catalog-backed route validation that checks course order, prerequisites, unknown courses, unknown skills, and final goal reachability.
- Pytest suite for data loading, goal parsing, planning, and validation.

## Project Structure

```text
PathCraft-AI-Career-Planner/
|-- data/                  # Skills and courses catalogs
|-- docs/                  # Technical report
|-- src/
|   |-- main.py            # CLI entry point
|   |-- planning/          # STRIPS model and A* search
|   |-- llm/               # Local natural-language goal parser and validation
|   `-- utils/             # Data loading and formatting helpers
|-- tests/                 # Automated tests
|-- requirements.txt
`-- README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python src/main.py --current_skills "Python fundamentals" --target "Data Scientist"
```

Other useful examples:

```bash
python src/main.py --current_skills skill_01 --target "Habilidad 12"
python src/main.py --current_skills "Python fundamentals, SQL querying" --target skill_12
python src/main.py --target "Quiero ser Data Scientist"
```

## Test

```bash
python -m pytest tests
```

## Notes

- The project intentionally avoids a mandatory external LLM dependency. The `src/llm` package implements the language-to-goal role locally so the planner remains reproducible offline.
- If an external LLM is required later, it should be added as an optional adapter and keep the current parser as the fallback.
