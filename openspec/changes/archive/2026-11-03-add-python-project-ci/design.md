## Context

Repositorio sin código: solo documentación, OpenSpec y un CI con el bloque Python comentado. ADR-0002 fija Python 3.12, uv y el paquete `src/logo_detector/`; ARCHITECTURE §4, §7 y §8 fijan la estructura, los comandos del `Makefile` y los checks del CI. Motivación en `proposal.md`.

## Goals / Non-Goals

**Goals:**

- Un único punto de verdad para dependencias y herramientas: `pyproject.toml`.
- Los mismos comandos en local y en el CI (`uv run ruff …`, `uv run pytest`), envueltos por el `Makefile`.
- Que `make install && make lint && make test` funcione en limpio en Linux (CI) y en Windows con Git Bash y GNU Make.

**Non-Goals:**

- Dependencias de visión (Ultralytics, OpenCV, FiftyOne) y Jupyter/jupytext: llegan con sus historias.
- Comprobación de tipos (mypy): ARCHITECTURE §8 no la incluye en el CI; se quita del bloque de la plantilla.
- Docker y `make docker-*` (S1.3).

## Decisions

- **Layout `src/` con backend `uv_build`.** El paquete se instala en modo editable con `uv sync`, y los tests importan el paquete instalado, no la carpeta. Alternativa: `hatchling`; `uv_build` es el backend por defecto de `uv init --package` y evita una herramienta más.
- **Python fijado con `requires-python = ">=3.12,<3.13"` y `.python-version` = `3.12`.** uv descarga 3.12 si no está instalado (en local hay 3.14), y el CI usa la misma versión. Alternativa: `>=3.12` abierto; ADR-0002 descarta 3.13+ por compatibilidad con PyTorch.
- **Dependencias de desarrollo en `[dependency-groups] dev`** (ruff, pytest), que `uv sync` instala por defecto. Alternativa: `optional-dependencies`; los grupos de dependencias son el estándar (PEP 735) y no se publican con el paquete.
- **ruff con reglas `E`, `F`, `I`, `UP`, `B`**, longitud de línea 100 y `target-version = "py312"`. Conjunto pequeño y útil: errores, imports ordenados, modernización y bugs habituales. Se amplía cuando haga falta.
- **`config.py` como constantes de módulo** con los valores por defecto de ARCHITECTURE §6: marcas (`coca-cola`, `pepsi`, `adidas`, DEC-01), rutas `data/`, `models/`, `outputs/` resueltas desde la raíz del repositorio, umbral de confianza 0,5 (RD-04) y tamaño de imagen 640 (valor por defecto de YOLO). Sin dependencias ni lógica; la sobrescritura por argumento la harán los componentes que la usen.
- **Test mínimo** que comprueba que el paquete se importa y expone una configuración coherente (umbral entre 0 y 1, tres marcas). Valida la cadena instalación → import → pytest sin inventar comportamiento.
- **CI:** se activa el bloque «Python con uv» en la raíz del repositorio (sin `working-directory`), con `uv sync --frozen`, `ruff check`, `ruff format --check` y `pytest`; se quitan mypy y `docker build` (este último lo añade S1.3) y los bloques de plantilla que no se usan (pip y Node).
- **`Makefile`** con `.PHONY` y objetivos `install` (`uv sync`), `lint` (`ruff check` + `ruff format --check`), `format` (`ruff format` + `ruff check --fix`) y `test` (`pytest`). `make lint` replica exactamente el CI.

## Risks / Trade-offs

- [El `Makefile` no funciona en Windows sin GNU Make] → El README indica el requisito; las recetas solo usan `uv`, sin comandos específicos de shell.
- [`uv.lock` desactualizado rompe `uv sync --frozen` en el CI] → Se genera y versiona en el mismo commit que `pyproject.toml`.
- [La versión de `astral-sh/setup-uv` de la plantilla no existe] → Se comprueba en el primer run del CI y se ajusta si falla.
