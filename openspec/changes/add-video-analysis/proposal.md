## Why

Historia [#13](https://github.com/Glezino/ai-computer-vision/issues/13), de la épica E4 (#5). La detección en imagen ya existe (#12), pero el producto analiza vídeos: hace falta aplicarla a cada fotograma, generar el vídeo anotado y entregar las detecciones por fotograma y los fps que necesita el informe de exposición (`report`, #11). Implementa RF-04 y comprueba RNF-02.

## What Changes

- Componente `detection` (`src/logo_detector/detection.py`):
  - análisis de un vídeo fotograma a fotograma con la detección en imagen existente y el mismo umbral configurable (50 % por defecto);
  - vídeo anotado en `outputs/<vídeo>_annotated.mp4` por defecto, con la misma resolución, los mismos fps y el mismo número de fotogramas que el original;
  - devuelve la ruta del vídeo anotado, los fps, las detecciones de cada fotograma (que `report.build_report` acepta tal cual) y el tiempo de procesado;
  - error claro si el archivo no existe o no es un vídeo legible.
- Tests con un vídeo sintético generado en el propio test y un modelo simulado (corren en el CI), y una medición del tiempo de procesado de un vídeo de 1 minuto con `brands.pt` en el equipo de la demo (RNF-02).

Fuera de alcance: el cálculo y la presentación del informe (ya existe `report`; la tabla y el JSON en la demo son de #14), el notebook de demo (#14), el audio del vídeo original y la reproducción del vídeo dentro del notebook.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `detection`: añade el análisis de vídeo (RF-04, RNF-02). Los requisitos de imagen no cambian.

## Impact

- **Código:** `src/logo_detector/detection.py` y `tests/test_detection.py`.
- **Dependencias:** ninguna nueva (OpenCV ya está).
- **Documentación:**
  - ARCHITECTURE: §3, `detection` pasa a «Actual»; §5, el flujo de análisis de vídeo según lo implementado; §8, los tests de vídeo y el tiempo medido frente a RNF-02.
  - ADR-0001: no se modifica.
- **Contratos:** ninguno; `report` y `detection` viven en el mismo paquete.
