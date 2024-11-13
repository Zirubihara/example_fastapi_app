# Makefile for FastAPI Application

# Variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
UVICORN = $(VENV_NAME)/bin/uvicorn
DOCKER_COMPOSE = docker-compose

# Default target
.PHONY: all
all: help

# Help
.PHONY: help
help:
	@echo "Makefile for FastAPI Application"
	@echo ""
	@echo "Usage:"
	@echo "  make install          Install dependencies"
	@echo "  make run             Run the FastAPI application"
	@echo "  make test            Run tests"
	@echo "  make docker-up       Start the Docker containers"
	@echo "  make docker-down     Stop the Docker containers"
	@echo "  make clean           Remove virtual environment"

# Install dependencies
.PHONY: install
install:
	python -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

# Run the FastAPI application
.PHONY: run
run:
	$(UVICORN) main:app --reload

# Run tests (you can customize this if you have a test suite)
.PHONY: test
test:
	$(PYTHON) -m unittest discover -s tests

# Start Docker containers
.PHONY: docker-up
docker-up:
	$(DOCKER_COMPOSE) up -d

# Stop Docker containers
.PHONY: docker-down
docker-down:
	$(DOCKER_COMPOSE) down

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV_NAME)