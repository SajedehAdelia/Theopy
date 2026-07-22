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
	@echo "    make upgrade              - Rebuild with the current requirements.txt, restart, and lint"
	@echo "    make docker-up            - Build and start the containers"
	@echo "    make docker-down          - Stop containers"
	@echo "    make docker-clean         - Remove all containers, images, and volumes"
	@echo "    make docker-exec          - Open a bash shell inside the container"
	@echo "    make docker-build                - Rebuild containers without starting"
	@echo "    make docker-logs                 - Follow container logs"
	@echo "  QUALITY & TESTING"
	@echo "    make format-black         - Automatically format code with Black"
	@echo "    make lint-flake8          - Check code style with Flake8"
	@echo "    make test                 - Run all tests inside the container"
	@echo "    make test-light           - Run only non-AI tests"
	@echo "    make test-full            - Run all tests with verbose output"
	@echo "    make test-js              - Run the frontend JS tests (host, no Docker/Node dependency in the image)"
	@echo "    make check                - Run format, lint, Python tests, and JS tests sequentially"
	@echo "  GITFLOW"
	@echo "    make git-feature name=xyz - Create a new feature branch from develop"

# --- Environment Management ---

install:
	@echo "Installing dependencies on local host..."
	pip3 install -r requirements.txt

docker-up:
	@echo "Starting system containers..."
	$(DOCKER_COMPOSE) up --build -d

upgrade:
	@echo "Rebuilding image against the current requirements.txt..."
	$(DOCKER_COMPOSE) build
	@echo "Restarting containers with the upgraded image..."
	$(DOCKER_COMPOSE) up -d
	@echo "Linting to confirm the upgrade didn't break style compliance..."
	$(MAKE) lint-flake8

docker-down:
	@echo "Stopping system containers..."
	$(DOCKER_COMPOSE) down

docker-clean:
	@echo "Performing deep clean of Docker environment..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

docker-exec:
	@echo "Opening shell in $(SERVICE_NAME)..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) /bin/bash

docker-build:
	@echo "Rebuilding images..."
	$(DOCKER_COMPOSE) build

docker-logs:
	@echo "Streaming logs..."
	$(DOCKER_COMPOSE) logs -f

# --- Quality Control & Testing ---

fix: format-black lint-flake8
	@echo "Optimization complete: Code formatted and linted."

format-black:
	@echo "Running Black formatter..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) black src/

lint-flake8:
	@echo "Checking PEP8 compliance..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) flake8 src/ --max-line-length=110

test:
	@echo "Running standard test suite..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/"

test-light:
	@echo "Running non-AI tests..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/ -m 'not ai' -v"

test-full:
	@echo "Running full test suite (including AI)..."
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "export PYTHONPATH=$(PYTHON_PATH) && pytest src/ -v"

test-js:
	@echo "Running frontend JS tests (Node's built-in test runner, no Docker needed)..."
	npm test

check: format-black lint-flake8 test test-js
	@echo "All quality checks passed: Code is formatted, linted, and tested (Python + JS)."

# --- Gitflow Helpers ---

git-feature:
	@echo "Creating new feature branch: feature/$(name)"
	git checkout develop || git checkout -b develop
	git checkout -b feature/$(name)