## 1. Imagen

- [x] 1.1 Escribir el `Dockerfile` (base `python:3.12-slim`, uv 0.11.24, librerías de OpenCV, `uv sync --frozen` en dos capas con el entorno en `/opt/venv`, `CMD` que genera los notebooks y arranca Jupyter Lab); verificar que `docker build -t logo-detector .` termina
- [x] 1.2 Escribir el `.dockerignore`; verificar que el contexto del *build* no incluye `.venv/`, `.git/` ni `models/` (tamaño del contexto en la salida de `docker build`)

## 2. Comandos

- [x] 2.1 Añadir `docker-build` y `docker-run` al `Makefile`; verificar desde Git Bash que `make docker-run` arranca Jupyter en `http://127.0.0.1:8888`, que `01_quickstart` se ejecuta de principio a fin y que los pesos quedan en `models/` del equipo

## 3. CI

- [x] 3.1 Añadir el job `docker` a `.github/workflows/ci.yml` con `docker build .`; verificar que pasa en verde en el PR

## 4. Documentación

- [x] 4.1 Documentar en el README el arranque con Docker (requisito: Docker; `make docker-build`, `make docker-run` y la URL de Jupyter)
- [x] 4.2 Actualizar ARCHITECTURE §2 (Docker pasa a «Actual») y revisar §7 y §8
