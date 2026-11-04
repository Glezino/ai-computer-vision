# ADR-0003: Descarga selectiva de OpenLogo con huggingface_hub

- **Estado:** Aceptado
- **Fecha:** 2026-11-03
- **Decisores:** Victor Gonzalez
- **Relacionado:** RF-01, #9, PROJECT DEC-02

## Contexto

OpenLogo está publicado en Hugging Face como `Voxel51/OpenLogo`, en formato FiftyOne: 27.083 imágenes (4,55 GB) y un `samples.json` de 25 MB con todas las anotaciones. Solo 1.725 imágenes (~0,3 GB) contienen Coca-Cola, Pepsi o Adidas. ARCHITECTURE preveía descargarlo con `fiftyone.utils.huggingface.load_from_hub`, pero esa función no filtra por etiqueta antes de descargar: baja el dataset entero. Además, FiftyOne necesita una base de datos MongoDB local.

## Decisión

- El componente `dataset` descarga primero `samples.json` con `huggingface_hub` y selecciona en Python las muestras de las tres marcas.
- Después descarga solo esas imágenes con `snapshot_download(allow_patterns=...)`.
- El repositorio se fija a una revisión concreta en `config.py` y los archivos se guardan en `data/openlogo/raw/`.
- FiftyOne no se añade como dependencia.

## Alternativas consideradas

- **FiftyOne `load_from_hub`:** el dataset completo son 15 veces más datos de los necesarios, y añade MongoDB a la instalación local, a Docker y a Colab.
- **Descarga desde la web de QMUL-OpenLogo:** un único archivo comprimido con todo el dataset, sin revisión fijada ni descarga parcial.

## Consecuencias

- Descarga de ~0,3 GB en lugar de 4,55 GB y una dependencia ligera (`huggingface-hub`).
- Resultado reproducible gracias a la revisión fijada.
- El código depende del esquema de `samples.json` de FiftyOne (`filepath`, `ground_truth.detections`, `bounding_box`). Si Voxel51 cambia el formato, hay que adaptar la lectura y actualizar la revisión.
- Sin la App de FiftyOne para explorar el dataset. Si se necesita, `samples.json` se puede cargar en FiftyOne aparte.
