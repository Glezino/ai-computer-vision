# AI Computer Vision — detector de logos en vídeo

Prueba de concepto que detecta logos de marcas (Coca-Cola, Pepsi y Adidas) en vídeos y genera un informe del tiempo y el porcentaje de aparición de cada una, para ayudar a una agencia de publicidad a decidir dónde invertir. Más contexto en [`docs/PROJECT.md`](docs/PROJECT.md).

## Estado

Hito 1 completo: el modelo reentrenado (YOLO26 nano, mAP@0.5 de validación 0,85) detecta las tres marcas en imágenes y vídeos, dibuja debajo de cada logo la marca y su confianza, y calcula el tiempo y el porcentaje de aparición de cada marca en un vídeo, que se guarda en JSON. Todo se recorre en el notebook de demo `03_demo`, en local o en Docker.

El trabajo se sigue en [GitHub Issues](https://github.com/Glezino/ai-computer-vision/issues) y las versiones se publican en [Releases](https://github.com/Glezino/ai-computer-vision/releases).

## Puesta en marcha

<!-- Requisitos y los dos o tres comandos para arrancar. El detalle operativo está en docs/ARCHITECTURE.md §7. -->

Requisitos: [uv](https://docs.astral.sh/uv/) y GNU Make (en Windows, desde Git Bash). uv descarga Python 3.12 si no está instalado.

```sh
make install   # crea el entorno e instala las dependencias
make lint      # ruff: lint y formato
make test      # pytest
```

Los notebooks se escriben como scripts `.py` en `notebooks/` y se generan como `.ipynb`, que no se versionan:

```sh
make notebooks       # genera notebooks/*.ipynb
uv run jupyter lab   # abre Jupyter; empieza por 01_quickstart
```

La primera ejecución de `01_quickstart` necesita internet para descargar los pesos preentrenados en `models/`.

Para entrenar hace falta el dataset de las tres marcas:

```sh
make data   # descarga de OpenLogo solo las imágenes de las marcas (~0,3 GB) y prepara data/openlogo/
```

### Modelo de marcas

La detección usa los pesos `models/brands.pt`, que no se versionan. Se obtienen entrenando en Google Colab con GPU (en CPU tardaría horas):

1. `make notebooks` y sube `notebooks/02_training.ipynb` a Colab (*Archivo → Subir cuaderno*); el navegador de GitHub de Colab no lo encuentra porque los `.ipynb` no se versionan.
2. *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU*. Si entrenas una rama distinta de `dev`, cámbiala en `BRANCH`.
3. *Ejecutar todo* (alrededor de una hora con una T4). Al terminar muestra las métricas y descarga `brands.pt`: cópialo a `models/`.

### Demo

Con los pesos en `models/brands.pt` y el dataset preparado (`make data`, para la imagen de ejemplo):

1. Deja uno o más vídeos en `data/videos/` (no se versionan); la demo usa `data/videos/demo.mp4`. Sirve cualquier `.mp4` corto, por ejemplo grabado con el móvil, con logos bien visibles.
2. `make notebooks`, abre Jupyter (`uv run jupyter lab` o, con Docker, `make docker-run`) y ejecuta todo `notebooks/03_demo.ipynb`.
3. Para otra imagen, otro vídeo u otro umbral de confianza (50 % por defecto), cambia la celda *Parámetros* y vuelve a ejecutar.

El notebook muestra la imagen anotada, el vídeo anotado, algunos fotogramas con detecciones y la tabla de exposición por marca. En `outputs/` deja `<vídeo>_annotated.mp4` (resolución original; se ve con VLC o similar), `<vídeo>_annotated.webm` (vista previa para el navegador) y `<vídeo>_report.json`. Un minuto de vídeo tarda alrededor de 1 minuto en CPU.

Para detectar las marcas en una imagen propia desde Python o un notebook:

```python
from logo_detector import detection

model = detection.load_model()
annotated, found = detection.detect_image(model, "mi_foto.jpg", threshold=0.5)
# annotated es la imagen anotada (BGR); found, las detecciones
print([detection.label(d) for d in found])  # p. ej. ['adidas 73 %']
```

### Con Docker

Requisitos: [Docker](https://docs.docker.com/get-docker/) y GNU Make; no hace falta instalar uv ni Python.

```sh
make docker-build   # construye la imagen de CPU (la primera vez tarda unos minutos)
make docker-run     # genera los notebooks y arranca Jupyter
```

Abre <http://127.0.0.1:8888/lab> (sin token; solo accesible desde tu equipo). El contenedor monta el repositorio, así que los cambios en `notebooks/*.py` y los pesos de `models/` se conservan en tu equipo.

El resto de comandos está en [`docs/ARCHITECTURE.md` §7](docs/ARCHITECTURE.md#7-entorno-local-y-operación).

## Contribuir

- [`WORKFLOW.md`](WORKFLOW.md): el flujo de trabajo de principio a fin y el mapa de documentación.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): ramas, commits, Issues, PRs y versiones.
- [`AGENTS.md`](AGENTS.md): instrucciones para agentes de IA.

## Licencia

Sin licencia definida.
