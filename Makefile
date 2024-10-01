.PHONY: install run run-backend run-frontend test lint format clean

# Poetry executable
POETRY := poetry

# Python executable (using Poetry's virtual environment)
PYTHON := $(POETRY) run python

# Project name
PROJECT_NAME := duffbot

# Install dependencies
install:
	$(POETRY) install

# Run the application (backend and frontend)
run: run-backend run-frontend

# Run the backend
run-backend:
	$(POETRY) run uvicorn backend.main:app --reload

# Run the frontend
run-frontend:
	$(POETRY) run python frontend/gradio_app.py

# Run tests
test:
	$(POETRY) run pytest

# Run linter
lint:
	$(POETRY) run flake8 backend frontend ai_agent tests

# Format code
format:
	$(POETRY) run black backend frontend ai_agent tests

# Clean up temporary files and caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.db" -delete


# Start a development shell
shell:
	$(POETRY) shell

# Generate requirements.txt (useful for environments that don't support Poetry)
requirements:
	$(POETRY) export -f requirements.txt --output requirements.txt

redis-flush:
	@echo "Flushing Redis database..."
	$(POETRY) run python -c "import redis; redis.Redis().flushall()"
	@echo "Redis database flushed."

build-backend-image:
	@echo "Building Docker image for backend..."
	docker build -t registry.digitalilusion.com/aibirras/duffbot-backend:latest -f backend.dockerfile .
	@echo "Docker image for backend built successfully."	

build-scoreboard-image:
	@echo "Building Docker image for scoreboard..."
	docker build -t registry.digitalilusion.com/aibirras/duffbot-scoreboard-fe:latest -f scoreboard.dockerfile .
	@echo "Docker image for scoreboard built successfully."	
	

push-backend-image:
	@echo "Push image for backend..."
	docker push registry.digitalilusion.com/aibirras/duffbot-backend:latest

push-scoreboard-image:
	@echo "Push image for scoreboard..."
	docker push registry.digitalilusion.com/aibirras/duffbot-scoreboard-fe:latest

rollout-backend:
	kubectl -n montevive rollout restart deployment duffbot-backend

rollout-gradio:
	kubectl -n montevive rollout restart deployment duffbot-gradio

rollout-scoreboard:
	kubectl -n montevive rollout restart deployment duffbot-scoreboard

deploy-scoreboard: build-scoreboard-image push-scoreboard-image rollout-scoreboard

help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies"
	@echo "  make run          - Run the application (backend and frontend)"
	@echo "  make run-backend  - Run the backend server"
	@echo "  make run-frontend - Run the frontend server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make clean        - Clean up temporary files and caches"
	@echo "  make shell        - Start a development shell"
	@echo "  make requirements - Generate requirements.txt"
	@echo "  make help         - Show this help message"
