## Context

OpenLogo está publicado en Hugging Face como `Voxel51/OpenLogo`, en formato FiftyOne:

- Tiene 27.083 imágenes JPG (4,55 GB) en `data/data_N/` y un `samples.json` de 25 MB con todas las anotaciones.
- Cada muestra trae `filepath`, `split` (`train` o `test`) y `ground_truth.detections` con `label` y `bounding_box` en `[x, y, w, h]` relativos a la esquina superior izquierda.

Se ha comprobado sobre `samples.json`:

- 1.725 imágenes contienen alguna de las ocho etiquetas de las tres marcas.
- 10 imágenes tienen más de una marca y 89 incluyen además logos de otras marcas.
- No hay cajas fuera de rango ni nombres de archivo repetidos.

`config.py` ya define `BRANDS = ("coca-cola", "pepsi", "adidas")` y `DATA_DIR`. Motivación en `proposal.md`; comportamiento en `specs/dataset/spec.md`.

## Goals / Non-Goals

**Goals:**

- Descargar lo mínimo y que una segunda ejecución no vuelva a descargar nada.
- Que la lógica (selección, conversión, división y estadísticas) sea pura y se pruebe sin red.

**Non-Goals:**

- Revisar a mano la calidad de las anotaciones de OpenLogo.
- Usar más datasets para RNF-03: se valorará con las métricas de #10.
- Aumento de datos: lo hace Ultralytics al entrenar (ADR-0001).

## Decisions

- **Descarga selectiva con `huggingface_hub` (ADR-0003).** Se baja `samples.json` con `hf_hub_download`, se seleccionan las muestras y se bajan solo sus imágenes con `snapshot_download(allow_patterns=[...])`, que descarga en paralelo. Todo queda en `data/openlogo/raw/`, así que una segunda ejecución lo reutiliza. Alternativa: FiftyOne `load_from_hub`; descarga el dataset completo y añade MongoDB.
- **Revisión fijada del repositorio.** El repositorio, `Voxel51/OpenLogo`, se fija a un commit concreto del dataset en `config.py`, para que el resultado sea reproducible aunque el dataset cambie en Hugging Face.
- **Etiquetas → clases** en un diccionario `OPENLOGO_LABELS` del módulo `dataset`. Los índices de clase siguen el orden de `config.BRANDS`: 0 Coca-Cola, 1 Pepsi y 2 Adidas. Las cajas de etiquetas que no están en el diccionario se descartan, y las imágenes sin ninguna caja de marca se excluyen.
- **Conversión a YOLO:** `[x, y, w, h]` → `[x + w/2, y + h/2, w, h]`, recortado a `[0, 1]` por seguridad. Es una función pura y se prueba con TDD.
- **Duplicados por contenido.** OpenLogo agrega siete datasets, así que puede haber la misma imagen con otro nombre. Tras descargar, se calcula el SHA-256 de cada imagen y, si varias coinciden, se queda solo la primera por orden de `filepath`, sin unir sus anotaciones. Así las particiones no comparten imágenes aunque estén repetidas en el origen.
- **División estratificada 70/15/15 con semilla fija.**
  - Cada imagen se asigna a la marca menos frecuente de las que contiene, de modo que las imágenes con varias marcas cuentan para la marca escasa.
  - Dentro de cada marca, las imágenes se ordenan por `filepath`, se barajan con `random.Random(seed)` y se cortan al 70 % y al 85 %.
  - Se ignora el `split` de OpenLogo, por decisión de producto.
  - Proporciones (`SPLIT_RATIOS = (0.7, 0.15, 0.15)`) y semilla (`SPLIT_SEED = 42`) se definen en `config.py`.
- **Estructura de salida** según la convención de Ultralytics:
  - `data/openlogo/images/{train,val,test}/` con las imágenes, copiadas desde `raw/`;
  - `data/openlogo/labels/{train,val,test}/` con un `.txt` por imagen;
  - `data/openlogo/data.yaml`, con `path` absoluto a `data/openlogo`, las rutas de cada partición y `names` con las tres marcas.

  Se usa ruta absoluta porque Ultralytics resuelve las rutas relativas contra su propio directorio de datasets. Antes de escribir, se borran las carpetas `images/` y `labels/` para no dejar restos de ejecuciones anteriores; `raw/` se conserva.
- **Estadísticas:** una función pura cuenta imágenes y cajas por marca y partición. El comando las imprime como tabla, con los totales de cada partición.
- **Punto de entrada:** `python -m logo_detector.dataset`, envuelto por `make data`. Usa logs en consola, como prevé ARCHITECTURE §8.
- **Tests (pytest, sin red)** con muestras construidas a mano:
  - conversión de cajas;
  - agrupación de variantes y descarte de otros logos;
  - exclusión de imágenes sin marcas;
  - eliminación de duplicados;
  - división: disjunta, determinista con la misma semilla y con proporciones por marca;
  - estadísticas.

  La descarga se comprueba a mano ejecutando `make data`.

## Risks / Trade-offs

- [Algunas imágenes contienen logos de las tres marcas sin anotar] → Es un límite de OpenLogo; se acepta en la prueba de concepto y se valorará con las métricas de #10.
- [Sin FiftyOne no se puede explorar el dataset en su App] → No hace falta para entrenar; si se necesitara más adelante, `samples.json` se puede cargar en FiftyOne.
- [El repositorio de Hugging Face cambia o desaparece] → La revisión está fijada en `config.py`; si desaparece, se documenta la descarga desde la web de QMUL-OpenLogo.
- [La licencia de investigación de OpenLogo] → Ya aceptada en PROJECT DEC-02. Las imágenes viven en `data/`, que no se versiona.
