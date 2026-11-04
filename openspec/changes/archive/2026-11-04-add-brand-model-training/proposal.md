## Why

Historia [#10](https://github.com/Glezino/ai-computer-vision/issues/10), la última de la épica E2 (#3). El dataset de las tres marcas ya existe (#9). Falta reentrenar el detector preentrenado para obtener unos pesos que usen la detección en imagen y vídeo (#12, #13). Implementa RF-02 y comprueba RNF-03 según [ADR-0001](../../../docs/ADR/0001-ultralytics-yolo-detector.md), que deja para esta historia la elección de la variante del modelo.

## What Changes

- Componente `training` (`src/logo_detector/training.py`):
  - configuración de entrenamiento explícita y versionada: tamaño de imagen, épocas, semilla y aumento de datos (flip, escala/crop, traslación, HSV y mosaic);
  - entrenamiento sobre `data/openlogo/data.yaml`, que copia los mejores pesos a `models/brands.pt`;
  - evaluación sobre validación con precisión, recall, mAP@0.5 y mAP@0.5:0.95, global y por marca.
- `notebooks/02_training.py` preparado para Google Colab con GPU: clona el repositorio, instala el paquete, prepara el dataset, entrena, muestra las métricas y descarga `brands.pt`. También se puede ejecutar en local.
- Modelo base: **YOLO26 nano** (`yolo26n.pt`), el mismo que el inicio rápido. Si no alcanza RNF-03, se prueba la variante small.
- Entrenamiento real en Colab, que ejecuta la persona porque necesita GPU. Las métricas obtenidas se documentan.

Fuera de alcance: búsqueda de hiperparámetros, publicación de los pesos como asset de release (fase de release) y la detección en imagen y vídeo (#12 y #13).

## Capabilities

### New Capabilities

- `training`: reentrenamiento del detector con las tres marcas, configuración reproducible y métricas de validación global y por marca (RF-02).

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `src/logo_detector/training.py`, `tests/test_training.py` y `notebooks/02_training.py`; `BRAND_MODEL` y `RUNS_DIR` en `config.py`.
- **Dependencias:** ninguna nueva (Ultralytics ya está).
- **Documentación:**
  - ARCHITECTURE: §3, `training` pasa a «Actual»; §7, cómo entrenar y dónde dejar los pesos; §8, las métricas obtenidas frente a RNF-03.
  - README: cómo obtener los pesos.
  - ADR-0001: no se modifica, ya que esta historia solo concreta la variante que ese ADR dejaba abierta.
- **Contratos:** ninguno.
