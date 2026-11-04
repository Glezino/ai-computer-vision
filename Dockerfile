# syntax=docker/dockerfile:1
# Imagen de CPU con el entorno de uv.lock y Jupyter Lab (ADR-0002, RNF-01).
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.24 /uv /uvx /bin/

# Librerías de sistema que necesita opencv-python en una imagen slim.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# El entorno vive fuera de /app para que montar el repositorio no lo oculte.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Dependencias en su propia capa: solo se reinstalan si cambian pyproject.toml o uv.lock.
# La caché de uv va en un cache mount para no quedarse en la imagen.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

EXPOSE 8888

# Genera los notebooks desde los .py (también los montados) y arranca Jupyter Lab.
CMD ["sh", "-c", "jupytext --to ipynb notebooks/*.py && exec jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --IdentityProvider.token=''"]
