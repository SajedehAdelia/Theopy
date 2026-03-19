# Theopy

Theopy is an AI-powered assistant project utilizing Gemini. This guide will help you set up your local development environment and run the system using Docker.

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

# Application port
PORT=8000

# PostgreSQL Database Configuration (pointing to Teepy's database)
POSTGRES_HOST=db_teepy
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password
```

**Note:** Theopy is designed to work alongside **Teepy**. For the database connection to work:
1. Both Teepy's and Theopy's Docker containers must be running.
2. Theopy and Teepy must be connected to the same Docker network. Theopy's `docker-compose.yml` is configured to use an external network named `teepy_default`. Teepy must create and use this network.

---

## Running with Docker

The easiest way to run the full Theopy system is via Docker. This ensures all services (Flask, AI logic, etc.) run in a consistent environment.

| Action | Command |
| --- | --- |
| **Start System** | `make docker-up` |
| **Stop System** | `make docker-down` |
| **View Logs** | `make logs` |
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
