# Comandos del proyecto (ARCHITECTURE §7). Requieren uv y GNU Make.
.PHONY: install lint format test

install:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest
