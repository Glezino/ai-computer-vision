# Comandos del proyecto (ARCHITECTURE §7). Requieren uv y GNU Make.
.PHONY: install lint format test notebooks docker-build docker-run

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

# Genera un .ipynb por cada notebooks/*.py (ADR-0002); los .ipynb no se versionan.
notebooks:
	uv run jupytext --to ipynb notebooks/*.py

# Imagen de CPU con Jupyter (ADR-0002). MSYS_NO_PATHCONV evita que Git Bash reescriba /app.
docker-build:
	docker build -t logo-detector .

docker-run:
	MSYS_NO_PATHCONV=1 docker run --rm -it -p 127.0.0.1:8888:8888 -v "$(CURDIR):/app" logo-detector
