## Why

Historia [#12](https://github.com/Glezino/ai-computer-vision/issues/12), la primera de la épica E4 (#5). Ya existen los pesos de las tres marcas (`models/brands.pt`, #10), pero ningún componente los aplica para mostrar qué marcas aparecen en una imagen. Implementa RF-03 y RD-04 según [ADR-0001](../../../docs/ADR/0001-ultralytics-yolo-detector.md), y sienta la base que reutilizará el análisis de vídeo (#13).

## What Changes

- Componente nuevo `detection` (`src/logo_detector/detection.py`):
  - carga del modelo de marcas desde `models/brands.pt`, con un error claro que indica cómo obtener los pesos si no existen;
  - detección en una imagen (ruta o matriz BGR) con umbral de confianza configurable, 50 % por defecto (`config.CONFIDENCE_THRESHOLD`);
  - dibujo de cada detección: bounding box, y debajo el nombre de la marca y su confianza en porcentaje (p. ej. `pepsi 87 %`);
  - devuelve la imagen anotada y la lista de detecciones (marca, confianza y caja), sin modificar la original.
- Tests unitarios del dibujo y del filtrado por umbral sin modelo, y un test de integración con `brands.pt` sobre una imagen de ejemplo que se salta si faltan los pesos o la imagen (no corre en el CI).

Fuera de alcance: vídeo y conversión a detecciones por fotograma para `report` (#13), y el notebook de demo (épica de demo).

## Capabilities

### New Capabilities

- `detection`: detección de las marcas en una imagen y anotación con bounding box, marca y confianza, con umbral configurable (RF-03, RD-04).

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `src/logo_detector/detection.py` y `tests/test_detection.py`.
- **Dependencias:** ninguna nueva (Ultralytics y OpenCV ya están).
- **Documentación:**
  - ARCHITECTURE: §3, `detection` pasa a «Actual» para imágenes (vídeo pendiente de #13); §8, tests de `detection`.
  - ADR-0001: no se modifica.
- **Contratos:** ninguno; todo vive en el mismo paquete.
