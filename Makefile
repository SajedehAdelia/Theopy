DOCKER_COMPOSE = docker compose
SERVICE_NAME = theopy

install:
	pip3 install -r requirements.txt

#  Start the whole system
docker-up:
	$(DOCKER_COMPOSE) up --build

#  Stop the system
docker-down:
	$(DOCKER_COMPOSE) down

#  Clean up images, containers, and volumes
docker-clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans

#  Enter the container's shell (to run commands manually inside)
docker-exec:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) /bin/bash

#  View live logs
logs:
	$(DOCKER_COMPOSE) logs -f

#  Run unit tests inside the container
test:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) pytest src/tests

#  Rebuild without starting 
build:
	$(DOCKER_COMPOSE) build

#  Gitflow Helper: Create a new feature branch
# Usage: make git-feature name=chatbox-logic
git-feature:
	git checkout develop || git checkout -b develop
	git checkout -b feature/$(name)

#  Help command to list available tasks
help:
	@echo "Theopy Project Management Commands:"
	@echo "  make docker-up            - Build and start the containers"
	@echo "  make docker-down          - Stop containers"
	@echo "  make docker-exec   - Open a bash shell inside the container"
	@echo "  make docker-clean  - Remove all containers, images, and volumes"
	@echo "  make logs          - Follow container logs"
	@echo "  make test          - Run pytest inside the container"
	@echo "  make git-feature name=xyz - Create a new feature branch from develop"