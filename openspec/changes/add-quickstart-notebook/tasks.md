## 1. Dependencias

- [x] 1.1 Añadir `ultralytics` y `opencv-python` a `[project] dependencies`, y `torch`/`torchvision` desde el índice de PyTorch CPU con `[tool.uv.sources]`; verificar que `uv lock` y `uv sync` terminan y que `uv run python -c "import torch; print(torch.__version__)"` muestra una versión `+cpu` (o sin CUDA)
- [x] 1.2 Añadir `jupyter` y `jupytext` al grupo `dev`; verificar con `uv run jupytext --version`
- [x] 1.3 Añadir `PRETRAINED_MODEL = "yolo26n.pt"` a `config.py`; verificar que `make lint` y `make test` pasan

## 2. Notebook de inicio rápido

- [x] 2.1 Escribir `notebooks/01_quickstart.py` en formato percent: cabecera en markdown, carga de `models/yolo26n.pt` (creando `models/`), predicción sobre `ASSETS / "bus.jpg"`, tabla de detecciones e imagen anotada; verificar que `make lint` pasa
- [x] 2.2 Añadir `.ipynb_checkpoints/` al `.gitignore`; verificar con `git status` tras abrir el notebook

## 3. Comando

- [x] 3.1 Añadir el objetivo `notebooks` al `Makefile` (`uv run jupytext --to ipynb notebooks/*.py`); verificar que genera `notebooks/01_quickstart.ipynb` y que no aparece en `git status`
- [x] 3.2 Ejecutar el notebook generado de principio a fin con `uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_quickstart.ipynb`; verificar que termina sin errores, que muestra detecciones y que los pesos quedan en `models/`

## 4. Documentación

- [x] 4.1 Documentar en el README cómo generar y abrir los notebooks (`make notebooks`, `uv run jupyter lab`, descarga de pesos en la primera ejecución)
- [x] 4.2 Actualizar ARCHITECTURE §2 (Ultralytics, PyTorch CPU, OpenCV, Jupyter y jupytext pasan a «Actual») y revisar §7
- [x] 4.3 Verificar en el PR que el job `python` del CI pasa en verde con las nuevas dependencias
