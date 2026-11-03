# ARCHITECTURE

> Cómo está construido el sistema y hacia dónde va. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

## 1. Visión general

Un paquete Python (`logo_detector`) agrupa todo el sistema. Sus módulos preparan el dataset, reentrenan un detector YOLO preentrenado, aplican el modelo a imágenes y vídeos, y calculan el informe de exposición. Los notebooks de demo (`.py` con jupytext, convertidos a `.ipynb` con `make`) solo orquestan esos módulos y muestran los resultados. El entrenamiento se ejecuta en una GPU de Google Colab; la inferencia y la demo, en local o en Docker con CPU.

```mermaid
flowchart LR
    OL[(OpenLogo<br/>Hugging Face)] --> DS[dataset]
    DS -->|imágenes + labels YOLO| TR[training]
    TR -->|pesos best.pt| DT[detection]
    IMG[/Imagen o vídeo/] --> DT
    DT -->|detecciones por fotograma| RP[report]
    DT --> OUT[/Imagen o vídeo anotado/]
    RP --> INF[/Informe JSON/]
    NB[notebooks] -.orquesta.-> DS & TR & DT & RP
```

## 2. Stack

| Área | Tecnología | Estado | Decisión |
|---|---|---|---|
| Lenguaje | Python 3.12 | Actual | [ADR-0002](ADR/0002-python-environment-and-notebooks.md) |
| Dependencias | uv (`pyproject.toml` + `uv.lock`) | Actual | [ADR-0002](ADR/0002-python-environment-and-notebooks.md) |
| Detector | Ultralytics YOLO, variante nano o small preentrenada en COCO | Actual | [ADR-0001](ADR/0001-ultralytics-yolo-detector.md) |
| Deep learning | PyTorch para CPU (índice de PyTorch), dependencia de Ultralytics | Actual | [ADR-0001](ADR/0001-ultralytics-yolo-detector.md) |
| Procesado de imagen y vídeo | OpenCV | Actual | [ADR-0001](ADR/0001-ultralytics-yolo-detector.md) |
| Descarga del dataset | FiftyOne (`load_from_hub`) | Objetivo | [PROJECT DEC-02](PROJECT.md#8-decisiones-de-producto) |
| Notebooks | Jupyter + jupytext (formato percent) | Actual | [ADR-0002](ADR/0002-python-environment-and-notebooks.md) |
| Entrenamiento | Google Colab con GPU | Objetivo | [ADR-0001](ADR/0001-ultralytics-yolo-detector.md) |
| Entorno de ejecución | Docker (imagen CPU) | Actual | [ADR-0002](ADR/0002-python-environment-and-notebooks.md) |
| Calidad | ruff, pytest | Actual | — |

## 3. Componentes

| Componente | Responsabilidad | Datos que posee | Depende de | Estado |
|---|---|---|---|---|
| `dataset` | Descarga OpenLogo, filtra las tres marcas, convierte las anotaciones a formato YOLO y crea las particiones (RF-01) | `data/` | OpenLogo, FiftyOne | Objetivo |
| `training` | Reentrena el detector con preprocesamiento y aumento de datos, y reporta métricas (RF-02) | `models/` (pesos), `runs/` | `dataset`, Ultralytics | Objetivo |
| `detection` | Aplica el modelo a imágenes y vídeos y dibuja bounding box, marca y confianza (RF-03, RF-04) | — | `training` (pesos), OpenCV | Objetivo |
| `report` | Calcula la exposición por marca a partir de las detecciones por fotograma (RF-05, RD-01…RD-04) | `outputs/` (informes) | `detection` | Objetivo |
| `notebooks` | Demo y presentación de punta a punta (RF-06) | — | Todos los anteriores | Objetivo |

`report` es lógica pura (detecciones → informe), sin dependencia del modelo, para poder probarla de forma aislada.

## 4. Estructura del repositorio

```text
.
├── src/logo_detector/   # dataset.py, training.py, detection.py, report.py, config.py
├── notebooks/           # *.py en formato jupytext; los .ipynb se generan y no se versionan
├── tests/
├── data/                # dataset descargado y preparado (no versionado)
├── models/              # pesos entrenados (no versionado; se publican como asset de release)
├── outputs/             # vídeos anotados e informes (no versionado)
├── Dockerfile
├── Makefile
├── pyproject.toml
├── docs/
└── openspec/
```

## 5. Flujos principales

### Análisis de un vídeo

```mermaid
sequenceDiagram
    participant N as notebook
    participant D as detection
    participant R as report
    N->>D: analizar(vídeo, pesos, umbral)
    loop cada fotograma
        D->>D: predecir y dibujar detecciones
    end
    D-->>N: vídeo anotado + detecciones por fotograma + fps
    N->>R: construir informe(detecciones, fps, nº fotogramas)
    R-->>N: informe por marca (s, %)
    N->>N: mostrar tabla y guardar JSON
```

Errores: si el archivo no se puede abrir como vídeo, `detection` lanza un error con un mensaje claro (RF-04). Si no existen los pesos, se indica cómo obtenerlos.

## 6. Datos, configuración y secretos

- **Persistencia:** archivos locales. `data/` guarda el dataset; `models/`, los pesos; `outputs/`, los vídeos anotados y los informes JSON. Nada de eso se versiona. No hay base de datos ([PROJECT §6](PROJECT.md#6-alcance)).
- **Configuración:** parámetros por defecto en `config.py` (marcas, rutas, umbral de confianza del 50 %, tamaño de imagen); se pueden sobrescribir por argumento.
- **Secretos:** ninguno. OpenLogo se descarga sin autenticación.
- **Datos enviados a terceros:** ninguno; solo se descargan el dataset y los pesos preentrenados.

## 7. Entorno local y operación

El `Makefile` es la fuente de verdad de los comandos. Los principales:

- `make install`: `uv sync`.
- `make notebooks`: genera los `.ipynb` desde `notebooks/*.py` con jupytext.
- `make data`: descarga y prepara el dataset.
- `make lint`, `make format` y `make test`: ruff (lint y formato) y pytest.
- `make docker-build` y `make docker-run`: construyen y arrancan el contenedor con Jupyter.

El entrenamiento se lanza desde el notebook de entrenamiento en Google Colab, que guarda `best.pt`; se copia a `models/`.

## 8. Calidad: tests, CI y observabilidad

- **Unitarios (pytest):** `report` (cálculo de exposición y reglas RD) y la conversión de anotaciones de `dataset`.
- **Integración:** detección sobre una imagen y un vídeo corto de ejemplo cuando haya pesos; no se ejecuta en el CI.
- **Calidad del modelo:** métricas de validación del entrenamiento (RNF-03), sin test automático.
- **CI:** `openspec validate`, ruff (lint y formato), pytest y `docker build`.
- **Observabilidad:** logs en consola y métricas de entrenamiento de Ultralytics en `runs/`.

## 9. Despliegue

No hay despliegue: el producto es una demo local con notebooks, ejecutable en Docker. Servir el modelo en cloud queda fuera de alcance ([PROJECT §6](PROJECT.md#6-alcance)).

## 10. Decisiones y contratos

- Decisiones técnicas: [índice de ADR](ADR/README.md).
- Interfaces estables: [índice de contratos](CONTRACTS/README.md). No hay contratos: todas las piezas viven en el mismo paquete.
