## Why

Historia [#9](https://github.com/Glezino/ai-computer-vision/issues/9), la primera de la épica E2 (#3). Para reentrenar el detector (RF-02, #10) hace falta un dataset de Coca-Cola, Pepsi y Adidas en formato YOLO y dividido en particiones. Implementa RF-01 con OpenLogo como dataset de partida (PROJECT DEC-01 y DEC-02).

## What Changes

- Componente `dataset` (`src/logo_detector/dataset.py`), que hace lo siguiente:
  - Descarga de Hugging Face (`Voxel51/OpenLogo`) los metadatos de OpenLogo y **solo las imágenes que contienen alguna de las tres marcas**, unas 1.725 imágenes y 0,3 GB de los 4,55 GB del total.
  - Agrupa las variantes de cada marca en una clase: `adidas`, `adidas1` y `adidas_text` → Adidas; `cocacola` y `coke` → Coca-Cola; `pepsi`, `pepsi_text` y `pepsi_text1` → Pepsi. Descarta las cajas de otros logos.
  - Convierte las anotaciones a formato YOLO.
  - Elimina las imágenes duplicadas y las divide en train, val y test (70/15/15), estratificadas por marca y con semilla fija.
  - Escribe `data/openlogo/` con imágenes, etiquetas y `data.yaml`, e imprime las imágenes y cajas por marca y partición.
- `make data` ejecuta todo el proceso.
- Dependencia `huggingface-hub`, que sustituye a la prevista FiftyOne.
- **ADR-0003**: descarga selectiva de OpenLogo con `huggingface_hub` en lugar de FiftyOne.

**Diferencia con la Issue:** la Issue preveía «descarga de OpenLogo con FiftyOne». Se ha decidido descargar solo las imágenes de las marcas con `huggingface_hub`, porque FiftyOne obliga a bajar el dataset entero y añade MongoDB como dependencia (ver ADR-0003).

Fuera de alcance: otros datasets, el entrenamiento (#10) y cualquier cambio de marcas.

## Capabilities

### New Capabilities

- `dataset`: preparación del dataset de las tres marcas para entrenar: filtrado, etiquetas, formato, particiones y estadísticas (RF-01).

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `src/logo_detector/dataset.py` y `tests/test_dataset.py`; parámetros del dataset (repositorio, semilla y proporciones) en `config.py`.
- **Dependencias:** `huggingface-hub` en `pyproject.toml` y `uv.lock`.
- **Comandos:** `Makefile` (`data`).
- **Documentación:**
  - ADR-0003 nuevo y su índice.
  - ARCHITECTURE: §2, la fila «Descarga del dataset» pasa a `huggingface_hub` con estado «Actual»; §3, `dataset` deja de depender de FiftyOne y pasa a «Actual».
  - README: `make data`.
- **Contratos:** ninguno. `data.yaml` sigue el formato de Ultralytics.
