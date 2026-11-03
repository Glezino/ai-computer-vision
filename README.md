# AI Computer Vision — detector de logos en vídeo

Prueba de concepto que detecta logos de marcas (Coca-Cola, Pepsi y Adidas) en vídeos y genera un informe del tiempo y el porcentaje de aparición de cada una, para ayudar a una agencia de publicidad a decidir dónde invertir. Más contexto en [`docs/PROJECT.md`](docs/PROJECT.md).

## Estado

El trabajo se sigue en [GitHub Issues](https://github.com/Glezino/ai-computer-vision/issues) y las versiones se publican en [Releases](https://github.com/Glezino/ai-computer-vision/releases).

## Puesta en marcha

<!-- Requisitos y los dos o tres comandos para arrancar. El detalle operativo está en docs/ARCHITECTURE.md §7. -->

Requisitos: [uv](https://docs.astral.sh/uv/) y GNU Make (en Windows, desde Git Bash). uv descarga Python 3.12 si no está instalado.

```sh
make install   # crea el entorno e instala las dependencias
make lint      # ruff: lint y formato
make test      # pytest
```

El resto de comandos está en [`docs/ARCHITECTURE.md` §7](docs/ARCHITECTURE.md#7-entorno-local-y-operación).

## Contribuir

- [`WORKFLOW.md`](WORKFLOW.md): el flujo de trabajo de principio a fin y el mapa de documentación.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): ramas, commits, Issues, PRs y versiones.
- [`AGENTS.md`](AGENTS.md): instrucciones para agentes de IA.

## Licencia

Sin licencia definida.
