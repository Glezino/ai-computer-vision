## Why

Historia [#6](https://github.com/Glezino/ai-computer-vision/issues/6) de la épica E1 (#2), walking skeleton. El repositorio aún no tiene código ejecutable: falta el paquete Python, las herramientas de calidad y sus checks en el CI, y de ello dependen las historias #7, #8, #9 y #11. Cubre en parte RNF-01 (entorno reproducible) según [ADR-0002](../../../docs/ADR/0002-python-environment-and-notebooks.md).

## What Changes

- `pyproject.toml` con Python 3.12 gestionado por uv, `uv.lock` versionado y `.python-version`.
- Paquete instalable `src/logo_detector/` con `config.py` (parámetros por defecto: marcas, rutas, umbral de confianza y tamaño de imagen).
- ruff (lint y formato) y pytest configurados en `pyproject.toml`, con un test mínimo en `tests/`.
- `Makefile` con `install`, `lint`, `format` y `test`.
- `.gitignore` de `data/`, `models/`, `outputs/`, `runs/`, `*.ipynb` y los artefactos de Python (`.venv/`, cachés).
- Bloque Python (uv) del CI activado: ruff check, ruff format --check y pytest.
- README: sección de puesta en marcha.

Fuera de alcance: notebooks y jupytext (S1.2, #7), Docker y su `docker build` en el CI (S1.3, #8), y las dependencias de Ultralytics, OpenCV y FiftyOne, que llegan con las historias que las usan.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

Ninguna. Es una historia `chore` sin cambio de comportamiento de producto: el cambio declara `skip_specs: true` y se archivará con `--skip-specs`.

## Impact

- **Código nuevo:** `pyproject.toml`, `uv.lock`, `.python-version`, `src/logo_detector/`, `tests/`, `Makefile`.
- **CI:** `.github/workflows/ci.yml` (job `python`).
- **Documentación:** `README.md` (puesta en marcha). ARCHITECTURE §4, §7 y §8 ya describen esta estructura; solo se ajusta si la implementación diverge.
- **ADR:** aplica ADR-0002; no requiere ADR nuevo.
- **Contratos:** ninguno.
