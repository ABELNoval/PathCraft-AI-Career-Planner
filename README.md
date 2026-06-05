# PathCraft: AI Career Path Planner

## Overview
This project solves the **Career Path Planning problem** (Theme 3). It generates a valid sequence of courses to transition from a current skill set to a professional goal.

## Key Features
1. **Natural Language Goal Setting:** Users define their career goals in plain English (e.g., "I want to become a Senior DevOps Engineer").
2. **Formal Planning Engine:** Uses a search-based approach (A*) to find the most efficient path through a skill-prerequisite graph.
3. **LLM Validation:** A Large Language Model verifies the semantic coherence of the generated path.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up your LLM API Key in a `.env` file.
3. Run the planner:
   ```bash
   python src/main.py --current_skills "Python, Basic Math" --target "Data Scientist"
