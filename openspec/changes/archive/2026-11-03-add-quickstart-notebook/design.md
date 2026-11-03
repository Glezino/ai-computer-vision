## Context

El paquete `logo_detector` solo tiene `config.py` y no declara dependencias; el CI ejecuta `uv sync --frozen`, ruff y pytest. `.gitignore` ya excluye `*.ipynb`, `models/` y `runs/`. ADR-0001 fija Ultralytics YOLO (nano o small, COCO) con inferencia en CPU; ADR-0002 fija jupytext en formato *percent* y `make notebooks`. Motivación en `proposal.md`; comportamiento en `specs/notebooks/spec.md`.

## Goals / Non-Goals

**Goals:**

- Validar de extremo a extremo la cadena entorno → Ultralytics → notebook en local, sin datos propios.
- Mantener el CI ligero pese a añadir PyTorch.

**Non-Goals:**

- Crear el componente `detection` ni funciones del paquete para el notebook: el inicio rápido usa la API de Ultralytics directamente y `detection` llega con RF-03 (#12).
- Ejecutar notebooks en el CI: requiere descargar pesos (ARCHITECTURE §8).
- Fijar el modelo definitivo de marcas: lo decide la historia de entrenamiento (ADR-0001).

## Decisions

- **PyTorch de CPU desde el índice de PyTorch.** Se declara `torch` y `torchvision` con `[tool.uv.sources]` apuntando a un `[[tool.uv.index]]` explícito `https://download.pytorch.org/whl/cpu`. Sin esto, en Linux (CI y Docker) uv instala la variante CUDA, con varios GB de librerías que nunca se usan: la inferencia es en CPU y el entrenamiento se hace en Colab con su propio entorno (ADR-0001). Alternativa: el PyTorch por defecto de PyPI; más simple, pero encarece el CI y la imagen de #8.
- **Dependencias del paquete:** `ultralytics` y `opencv-python` en `[project] dependencies`, porque los usarán `training` y `detection`. OpenCV ya llega con Ultralytics, pero se declara porque el código del paquete lo usará directamente (RF-04). **Jupyter y jupytext** van al grupo `dev`: son herramientas de la demo, no del paquete, y `uv sync` los instala por defecto.
- **Modelo preentrenado `yolo26n.pt`** (YOLO26 nano, el de la serie actual de Ultralytics 8.4), con su nombre en `config.PRETRAINED_MODEL`. Nano basta para CPU y es la base prevista por ADR-0001. Alternativa: `yolo11n.pt`; igual de válido, pero de una serie anterior.
- **Pesos en `models/`.** El notebook carga `config.MODELS_DIR / config.PRETRAINED_MODEL`; Ultralytics descarga el archivo en esa ruta si no existe. Así no se dejan pesos en `notebooks/` (el directorio de trabajo del kernel) y se reutilizan entre ejecuciones. Se crea `models/` si no existe.
- **Imagen de ejemplo de Ultralytics** (`ultralytics.utils.ASSETS / "bus.jpg"`), que viene dentro del paquete instalado: no hay que descargar ni versionar binarios. Alternativa: una imagen propia en el repositorio; añade un binario sin aportar nada en esta historia.
- **Visualización:** `results[0].plot()` dibuja cajas, clase y confianza; la imagen BGR se convierte a RGB y se muestra con `PIL.Image` (ya dependencia de Ultralytics), sin añadir matplotlib. El notebook también imprime una tabla breve de detecciones (clase y confianza) para que el resultado sea comprobable sin mirar la imagen.
- **`make notebooks`** = `uv run jupytext --to ipynb notebooks/*.py`. jupytext reescribe el `.ipynb` en cada ejecución, de modo que refleja el script actual. Se ejecuta desde Git Bash en Windows, como el resto del `Makefile`.
- **Calidad:** los `notebooks/*.py` son Python válido y pasan por `ruff check` y `ruff format` como el resto del código. Se añade `.ipynb_checkpoints/` al `.gitignore`.
- **Tests:** no hay lógica propia que probar con TDD. La ejecución de principio a fin se verifica a mano con `jupyter nbconvert --execute` (integración fuera del CI, ARCHITECTURE §8).

## Risks / Trade-offs

- [El índice de PyTorch CPU no tiene ruedas para alguna plataforma o versión de Python] → Se comprueba con `uv lock` y en el CI; si falla, se limita el índice a Linux con un marcador de entorno y se usa PyPI en Windows.
- [La primera ejecución necesita internet para descargar los pesos] → Se indica en el README; las siguientes reutilizan `models/`.
- [El CI tarda más por instalar Ultralytics y PyTorch] → Mitigado con PyTorch CPU y la caché de `setup-uv`.
- [Ultralytics escribe ajustes en el directorio del usuario y puede crear `runs/`] → `runs/` ya está en `.gitignore`; la predicción del notebook no guarda resultados en disco.
