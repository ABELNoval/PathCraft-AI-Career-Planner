# PathCraft: AI Career Path Planner

## Overview
This repository is now prepared as a full project template for the Theme 4 workflow. It includes the folder layout, placeholder data catalogs, planning modules, LLM modules, utilities, tests, and a report placeholder.

## Project Structure

## Main Entry Point
Run the template entry point with:

```bash
python src/main.py --current_skills "Python, Basic Math" --target "Data Scientist"
## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up your LLM API Key in a `.env` file`.
3. Run the planner:
	```bash
	python src/main.py --current_skills "Python, Basic Math" --target "Data Scientist"

Project skeleton added. Estructura creada:

```
PathCraft-AI-Career-Planner/
├── data/                   # Catálogos de cursos y habilidades
├── docs/                   # Informe técnico final
├── src/                    # Código fuente
│   ├── main.py             # Punto de entrada del planeador
│   ├── planning/           # Lógica de IA clásica
│   ├── llm/                # Componente de Lenguaje Natural
│   └── utils/              # Cargadores de datos y formateo
├── tests/                  # Instancias de prueba para experimentación
├── requirements.txt        # Librerías (NLTK, OpenAI/LangChain, etc.)
└── README.md               # Instrucciones de uso
```
```

## Next Steps
1. Fill `data/skills_library.json` and `data/courses_db.json` with the real catalog.
2. Replace the placeholders in `src/planning/` and `src/llm/` with the final logic.
3. Export the final report to `docs/technical_report.pdf`.
