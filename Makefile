# --- Variables ---
DOCKER_COMPOSE = docker compose
SERVICE_NAME = theopy
PYTHON_PATH = .

# --- Default Command ---
.PHONY: help
help:
	@echo "Theopy Project Management Commands:"
	@echo "  ENVIRONMENT"
	@echo "    make install              - Install dependencies on local host"
	@echo "    make docker-up            - Build and start the containers"
	@echo "    make docker-down          - Stop containers"
	@echo "    make docker-clean         - Remove all containers, images, and volumes"
	@echo "    make docker-exec          - Open a bash shell inside the container"
	@echo "    make build                - Rebuild containers without starting"
	@echo "    make logs                 - Follow container logs"
	@echo "  QUALITY & TESTING"
	@echo "    make format               - Automatically format code with Black"
	@echo "    make lint                 - Check code style with Flake8"
	@echo "    make test                 - Run all tests inside the container"
	@echo "    make test-light           - Run only non-AI tests"
	@echo "    make test-full            - Run all tests with verbose output"
	@echo "    make check                - Run format, lint, and tests sequentially"
	@echo "  GITFLOW"
	@echo "    make git-feature name=xyz - Create a new feature branch from develop"

# --- Environment Management ---

install:
	@echo "Installing dependencies on local host..."
	pip3 install -r requirements.txt

docker-up:
	@echo "Starting system containers..."
	$(DOCKER_COMPOSE) up --build -d

docker-down:
	@echo "Stopping system containers..."
	$(DOCKER_COMPOSE) down

docker-clean:
	@echo "Performing deep clean of Docker environment..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

docker-exec:
	@echo "Opening shell in $(SERVICE_NAME)..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) /bin/bash

build:
	@echo "Rebuilding images..."
	$(DOCKER_COMPOSE) build

logs:
	@echo "Streaming logs..."
	$(DOCKER_COMPOSE) logs -f

# --- Quality Control & Testing ---

format:
	@echo "Running Black formatter on src/..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) black src/

lint:
	@echo "Running Flake8 linter on src/..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) flake8 src/ --max-line-length=100

test:
	@echo "Running standard test suite..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/"

test-light:
	@echo "Running non-AI tests..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/ -m 'not ai' -v"

test-full:
	@echo "Running full test suite (including AI)..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/ -v"

check: format lint test
	@echo "All quality checks passed: Code is formatted, linted, and tested."

# --- Gitflow Helpers ---

git-feature:
	@echo "Creating new feature branch: feature/$(name)"
	git checkout develop || git checkout -b develop
	git checkout -b feature/$(name)