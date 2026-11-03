## Why

Historia [#8](https://github.com/Glezino/ai-computer-vision/issues/8) de la épica E1 (#2), walking skeleton. El proyecto ya tiene entorno con uv (#6) y un notebook de inicio rápido (#7), pero ejecutarlo exige instalar uv, Python y GNU Make en el equipo. Cubre RNF-01 (reproducibilidad con Docker) según [ADR-0002](../../../docs/ADR/0002-python-environment-and-notebooks.md).

## What Changes

- `Dockerfile` de CPU: Python 3.12, uv y el entorno instalado desde `uv.lock`; al arrancar genera los notebooks y abre Jupyter Lab.
- `.dockerignore` para no copiar al contexto el entorno local, Git, datos, pesos ni resultados.
- `make docker-build` y `make docker-run`.
- Job `docker` en el CI que construye la imagen en cada PR.
- README: cómo arrancar el proyecto con Docker.

Fuera de alcance: imagen con GPU, publicación de la imagen en un registro y despliegue en cloud ([PROJECT §6](../../../docs/PROJECT.md#6-alcance)).

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

Ninguna. Es una historia `chore` de infraestructura sin cambio de comportamiento de producto: el cambio declara `skip_specs: true` y se archivará con `--skip-specs`.

## Impact

- **Código nuevo:** `Dockerfile`, `.dockerignore`.
- **Comandos:** `Makefile` (`docker-build`, `docker-run`).
- **CI:** `.github/workflows/ci.yml` (job `docker`).
- **Documentación:** `README.md` (puesta en marcha con Docker); ARCHITECTURE §2 (Docker pasa a «Actual») y revisión de §7 y §8.
- **ADR:** aplica ADR-0002; no requiere ADR nuevo.
- **Contratos:** ninguno.
