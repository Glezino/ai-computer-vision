## 1. Base

- [x] 1.1 Añadir `huggingface-hub` a las dependencias y a `config.py` el repositorio y la revisión de OpenLogo, `SPLIT_RATIOS` y `SPLIT_SEED`; verificar que `uv sync`, `make lint` y `make test` pasan
- [x] 1.2 Escribir ADR-0003 (descarga selectiva de OpenLogo con `huggingface_hub`) y añadirlo al índice de ADR

## 2. Lógica del dataset (TDD)

- [x] 2.1 Conversión de caja `[x, y, w, h]` a YOLO con recorte a `[0, 1]`; verificar con tests en `tests/test_dataset.py`
- [x] 2.2 Selección de muestras: agrupar variantes en las tres marcas, descartar otros logos y excluir imágenes sin marcas; verificar con tests
- [x] 2.3 Eliminación de duplicados por hash de contenido; verificar con tests
- [x] 2.4 División 70/15/15 estratificada por marca y con semilla; verificar con tests que es disjunta, determinista y respeta las proporciones por marca
- [x] 2.5 Estadísticas de imágenes y cajas por marca y partición; verificar con tests

## 3. Descarga, escritura y comando

- [x] 3.1 Descargar `samples.json` y las imágenes seleccionadas en `data/openlogo/raw/` con `huggingface_hub`; verificar que una segunda ejecución no vuelve a descargar
- [x] 3.2 Escribir `images/`, `labels/` y `data.yaml` en `data/openlogo/` e imprimir la tabla de estadísticas; añadir `make data`; verificar ejecutando `make data`
- [x] 3.3 Comprobar sobre el resultado real que solo hay clases 0–2, que las particiones no comparten imágenes ni hashes, que las proporciones por marca se acercan a 70/15/15 y que Ultralytics lee el `data.yaml` (`ultralytics.data.utils.check_det_dataset`)

## 4. Documentación

- [x] 4.1 Actualizar ARCHITECTURE §2 (descarga con `huggingface_hub`, «Actual») y §3 (`dataset` sin FiftyOne, «Actual»), y añadir `make data` al README
