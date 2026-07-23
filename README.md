# Theopy

Theopy is an AI-powered assistant project utilizing Gemini, built by [Kozea](https://kozea.fr). It connects to **[Teepy](https://github.com/Kozea/teepy)**, Kozea's pharmacy-management ERP, via the Model Context Protocol (MCP), letting users query and act on real Teepy data through natural language.

Teepy's repository is private. A sanitized extract of my MCP/authentication contribution to Teepy - real file structure, only my own code kept - is public here: **[teepy-mcp-contribution](https://github.com/SajedehAdelia/teepy-mcp-contribution)**.

**Note on running this locally:** Theopy needs a running instance of Teepy to talk to (see "Local Setup" below). Since Teepy is Kozea's private, proprietary codebase, you likely won't be able to clone and run it yourself unless you already have access. To see the full system working end-to-end regardless, a short demo video is included: **[demo video link here](https://github.com/user-attachments/assets/f473e4ca-4176-405b-8a93-f59ebab511e8)**.

This guide will help you set up your local development environment and run the system using Docker.

##  Prerequisites

* **Python 3.11+**
* **Docker & Docker Compose**
* **Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))

---

##  Local Setup (Virtual Environment)

Before running the project, set up a local virtual environment to isolate your dependencies and avoid "Externally Managed Environment" errors.

1. **Create and Activate the Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate

```


2. **Install Dependencies**
Once the environment is active (you see `(.venv)` in your terminal), run:
```bash
make install

```


3. **Configure Environment Variables**
Create a `.env` file in the root directory. This file contains API keys and the database connection details required to communicate with Teepy:

```text
# Gemini API key from Google AI Studio
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL_ID=gemini-2.5-flash

# Application port
PORT=8000

# Flask session signing key - required for login
SECRET_KEY=generate_a_random_value_here

# PostgreSQL Database Configuration (pointing to Teepy's database)
POSTGRES_HOST=db_teepy
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password

# Teepy's MCP server (tool calls) and HTTP API (login authentication) - two
# different ports on the same Teepy container
TEEPY_MCP_URL=http://teepy-app-1:5001/sse
TEEPY_API_URL=http://teepy-app-1:5000

# Optional: run fully local/offline with Ollama instead of Gemini
USE_LOCAL_LLM=0
OLLAMA_MODEL=llama3.1
```

**Note:** Theopy is designed to work alongside **Teepy**. For the database connection to work:
1. Both Teepy's and Theopy's Docker containers must be running.
2. Theopy and Teepy must be connected to the same Docker network. Theopy's `docker-compose.yml` is configured to use an external network named `teepy_default`. Teepy must create and use this network.

**Logging in:** Theopy has no signup - it authenticates against real Teepy
accounts. Log in at `http://localhost:8000/login` with an existing Teepy
login/password. Only Kozea staff roles (administrator, manager, operator,
commercial, contractor) can access Theopy; the `employee` role (external
pharmacy portal accounts) is rejected.

---

## Running with Docker

The easiest way to run the full Theopy system is via Docker. This ensures all services (Flask, AI logic, etc.) run in a consistent environment.

| Action | Command |
| --- | --- |
| **Start System** | `make docker-up` |
| **Stop System** | `make docker-down` |
| **View Logs** | `make docker-logs` |
| **Run Tests** | `make test` |
| **Reset/Clean** | `make docker-clean` |

---

##  Development Workflow

### Creating a New Feature

We use a Gitflow-inspired branching model. To start a new feature:

```bash
make git-feature name=your-feature-name

```

### Accessing the Container

If you need to run commands manually inside the running container:

```bash
make docker-exec

```
