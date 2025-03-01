# Makefile for FastAPI Application


# Variables
VENV_NAME = venv
PYTHON = python
PIP = pip
PYTEST = pytest
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
	@echo "  make format          Format code"
	@echo "  make lint            Lint code"
	@echo "  make coverage        Generate test coverage"
	@echo "  make migrate         Run database migrations"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Run the FastAPI application
.PHONY: run
run:
	$(UVICORN) main:app --reload

# Run tests (you can customize this if you have a test suite)
.PHONY: test
test:
	$(PYTEST) tests -v --disable-warnings

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
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Format code
.PHONY: format
format:
	black app tests main.py
	isort app tests main.py

# Lint code
.PHONY: lint
lint:
	flake8 app tests main.py
	black --check app tests main.py
	isort --check-only app tests main.py

# Generate test coverage
.PHONY: coverage
coverage:
	$(PYTEST) --cov=app tests/ --cov-report=term-missing --disable-warnings

# Run database migrations
.PHONY: migrate
migrate:
	$(PYTHON) -m alembic upgrade head

# Test commands
.PHONY: test-cov
test-cov:
	$(PYTEST) --cov=app tests/ --cov-report=term-missing --disable-warnings