# Build Your First Agent with Google ADK

A math tutor AI agent built with Google's Agent Development Kit (ADK), completed as part of the
Google Skills course "Build Your First Agent with Agent Development Kit (ADK)".

## What's inside

| Path | What it is |
|---|---|
| `my_first_agent/` | Agent in **Python** with two tools: `solve_linear_equation` and `check_answer` |
| `my_config_agent/` | Same tutor defined in **YAML** (`root_agent.yaml`) |
| `run_agent.py` | Runs an agent **programmatically** with `Runner` + `InMemorySessionService` |

The tutor guides students step by step instead of giving answers. It uses its tools to
verify the correct solution and to check each answer the student proposes.

## Setup

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

Create a `.env` file in each agent folder (key from https://aistudio.google.com/apikey):

    GOOGLE_GENAI_USE_VERTEXAI=0
    GOOGLE_API_KEY=your-key-here

## Run it

| Method | Command |
|---|---|
| Web UI | `adk web` then open http://127.0.0.1:8000 |
| Terminal | `adk run my_first_agent` |
| REST API | `adk api_server` |
| Python | `python run_agent.py` |

Try: "How do I solve 2x + 5 = 13?" then "Is x = 4?"

## Concepts covered
- Agent = Model + Tools + Orchestration
- `model`, `name`, `description` (for other agents), `instruction` (for this agent)
- `root_agent` is the entry point ADK looks for
- Python code vs YAML Agent Config
