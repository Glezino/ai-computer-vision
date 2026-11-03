## 1. Paquete y dependencias

- [x] 1.1 Crear `pyproject.toml` (Python 3.12, backend `uv_build`, grupo `dev` con ruff y pytest) y `.python-version`; verificar que `uv sync` genera `uv.lock` y crea el entorno con Python 3.12
- [x] 1.2 Crear `src/logo_detector/__init__.py` y `config.py` con marcas, rutas, umbral y tamaño de imagen por defecto; verificar con `uv run python -c "import logo_detector.config"`

## 2. Calidad

- [x] 2.1 Configurar ruff (reglas, longitud de línea, `target-version`) y pytest (`testpaths`) en `pyproject.toml`; verificar que `uv run ruff check .` y `uv run ruff format --check .` pasan
- [x] 2.2 Añadir `tests/test_config.py` que importa el paquete y comprueba la configuración por defecto; verificar que `uv run pytest` pasa

## 3. Comandos y repositorio

- [x] 3.1 Crear el `Makefile` con `install`, `lint`, `format` y `test`; verificar que cada objetivo termina con éxito
- [x] 3.2 Añadir al `.gitignore` `data/`, `models/`, `outputs/`, `runs/`, `*.ipynb`, `.venv/` y cachés de Python; verificar con `git status` que no aparecen archivos generados

## 4. CI

- [ ] 4.1 Activar en `.github/workflows/ci.yml` el job `python` con uv en la raíz (ruff check, ruff format --check, pytest) y quitar los bloques de plantilla no usados; verificar que el job pasa en verde en el PR

## 5. Documentación

- [x] 5.1 Escribir la puesta en marcha del README (requisitos: uv y GNU Make; comandos `make install`, `make lint`, `make test`) y revisar que ARCHITECTURE §4, §7 y §8 siguen siendo correctas
- [x] 5.2 Verificar en limpio (sin `.venv/`) que `make install && make lint && make test` funciona
