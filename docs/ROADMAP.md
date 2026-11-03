# ROADMAP

> En qué orden se construye el producto: hitos, épicas y dependencias entre ellas. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

## Dirección

Primero, un esqueleto ejecutable (paquete, notebooks, Docker y CI) que detecta objetos con el modelo preentrenado. Después, el modelo de marcas y, sobre él, el análisis de vídeo con su informe de exposición. El cálculo del informe es lógica independiente del modelo y puede avanzar en paralelo.

## Hito 1 — Prueba de concepto entregable

**Resultado:** a partir de un vídeo, la demo en notebook muestra el vídeo anotado con las marcas y su confianza, y el informe de exposición por marca, reproducible en Docker.

### E1 — Walking skeleton: paquete, notebooks, Docker y CI · Issue: pendiente

- **Resultado:** `make notebooks` genera un notebook que detecta objetos en una imagen con el YOLO preentrenado en COCO, en local y en Docker; el CI ejecuta ruff, pytest y `docker build`.
- **Requisitos:** RF-06, RNF-01
- **Depende de:** —

### E2 — Modelo de detección de marcas · Issue: pendiente

- **Resultado:** dataset de las tres marcas preparado y modelo reentrenado con sus métricas de validación; los pesos quedan disponibles en `models/`.
- **Requisitos:** RF-01, RF-02, RNF-03
- **Depende de:** E1, porque usa su paquete, su entorno y sus notebooks.

### E3 — Informe de exposición · Issue: pendiente

- **Resultado:** a partir de las detecciones por fotograma se calcula el tiempo y el porcentaje de aparición de cada marca y se guarda en JSON.
- **Requisitos:** RF-05, RD-01, RD-02, RD-03, RD-04
- **Depende de:** E1, porque usa su paquete y su CI. No depende del modelo: trabaja con detecciones de ejemplo.

### E4 — Detección de marcas en imagen y vídeo · Issue: pendiente

- **Resultado:** el notebook de demo anota imágenes y vídeos con bounding box, marca y confianza, y muestra el informe de exposición del vídeo.
- **Requisitos:** RF-03, RF-04, RNF-02
- **Depende de:** E2, porque necesita los pesos entrenados; y E3, porque muestra su informe.
