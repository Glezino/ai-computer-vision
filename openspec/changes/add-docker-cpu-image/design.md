## Context

El entorno se define en `pyproject.toml` y `uv.lock`: PyTorch de CPU desde el índice de PyTorch (con ruedas para Linux x86_64 y aarch64), Ultralytics, OpenCV y, en el grupo `dev`, Jupyter y jupytext. `make notebooks` genera los `.ipynb` y el notebook `01_quickstart` descarga sus pesos en `models/`. ARCHITECTURE §7 ya prevé `make docker-build` y `make docker-run`, y §8 un `docker build` en el CI. Motivación en `proposal.md`.

## Goals / Non-Goals

**Goals:**

- Una imagen que reproduce exactamente el entorno de `uv.lock` y arranca Jupyter con el proyecto.
- Que los pesos descargados y los resultados persistan entre ejecuciones del contenedor.
- Reconstrucciones rápidas cuando solo cambia el código.

**Non-Goals:**

- Ejecutar el notebook ni los tests dentro de la imagen en el CI: el CI solo la construye.
- Optimizar al máximo el tamaño (imagen multietapa, *distroless*).
- Usuario sin privilegios ni endurecimiento: es una demo local.

## Decisions

- **Base `python:3.12-slim` y uv copiado de su imagen oficial con versión fija** (`COPY --from=ghcr.io/astral-sh/uv:0.11.24`, la versión usada en local). Alternativa: la imagen `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`; equivalente, pero fijar uv por separado deja clara su versión y la base de Python es la oficial.
- **Librerías de sistema para OpenCV** (`libgl1`, `libglib2.0-0`): `opencv-python` las necesita para importarse en una imagen *slim*. Alternativa: `opencv-python-headless`; lo descartamos porque Ultralytics declara `opencv-python` y acabarían instaladas las dos variantes.
- **Instalación en dos capas:** primero `pyproject.toml` y `uv.lock` con `uv sync --frozen --no-install-project`, y después el código con `uv sync --frozen`. Las dependencias pesadas (PyTorch, Ultralytics) quedan en caché de Docker y solo se reinstala el proyecto al cambiar el código. Se incluye el grupo `dev` porque contiene Jupyter y jupytext. La caché de uv va en un *cache mount* de BuildKit (`--mount=type=cache`), así no se queda en la imagen (sin él ocupaba 1,5 GB más) y además acelera las reconstrucciones.
- **Entorno fuera del directorio de trabajo** (`UV_PROJECT_ENVIRONMENT=/opt/venv`, con `/opt/venv/bin` en el `PATH`). Así, montar el repositorio en `/app` no oculta el entorno y el `.venv/` de Windows del equipo nunca se usa dentro del contenedor.
- **`make docker-run` monta el repositorio en `/app`.** Los notebooks reflejan los `.py` del equipo, y `models/`, `outputs/` y los `.ipynb` generados persisten en el equipo (todos ignorados por Git). El paquete está instalado en modo editable desde `/app/src`, de modo que también ve el código montado. Sin montaje, la imagen sigue siendo autosuficiente con la copia del código del momento del *build*.
- **Arranque:** el `CMD` ejecuta `jupytext --to ipynb notebooks/*.py` y después `jupyter lab --ip=0.0.0.0 --no-browser --allow-root`. Se generan al arrancar, y no en el *build*, para que reflejen los scripts montados.
- **Acceso a Jupyter sin token, publicado solo en `127.0.0.1:8888`.** El README da una URL directa y nadie fuera del equipo puede conectarse. Alternativa: mantener el token; más seguro en redes compartidas, pero obliga a copiar la URL de los logs en cada arranque. Al ser una demo local, se prioriza la sencillez.
- **Comandos de `make`:** `docker-build` = `docker build -t logo-detector .`; `docker-run` = `docker run --rm -it -p 127.0.0.1:8888:8888 -v "$(CURDIR):/app" logo-detector`, con `MSYS_NO_PATHCONV=1` para que Git Bash en Windows no reescriba la ruta `/app`. La variable no tiene efecto en Linux ni en macOS.
- **CI:** nuevo job `docker` que ejecuta `docker build .` en `ubuntu-latest`, en paralelo al job `python`. Alternativa: `docker/build-push-action` con caché de GitHub Actions; se añadirá si el *build* se vuelve lento.
- **`.dockerignore`:** `.git/`, `.venv/`, cachés de Python, `data/`, `models/`, `outputs/`, `runs/`, `*.ipynb`, `.ipynb_checkpoints/` y las carpetas de las integraciones de IA. Reduce el contexto y evita copiar pesos o datos a la imagen.

## Risks / Trade-offs

- [La imagen ocupa más de 1 GB por PyTorch y Ultralytics] → PyTorch de CPU (sin CUDA) y capas cacheadas; se acepta en una demo local.
- [En Linux los archivos que crea el contenedor en el montaje son de root] → Solo afecta a archivos ignorados (`models/`, `outputs/`, `.ipynb`); se documenta y se puede pasar `--user` si molesta.
- [Docker Desktop no está arrancado en el equipo de desarrollo] → El *build* se verifica en el CI; la ejecución local (`make docker-run` y abrir el notebook) se comprueba arrancando Docker Desktop antes de la Parada 3.
- [El primer `docker-run` necesita internet para los pesos] → Igual que fuera de Docker; tras la primera vez quedan en `models/` del equipo.
