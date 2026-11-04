# notebooks Specification

## Purpose

Notebooks de demo y presentación del proyecto, mantenidos como scripts `.py` y generados como `.ipynb` bajo demanda (RF-06, PROJECT DEC-05).

## Requirements

### Requirement: Generación de notebooks desde scripts

El sistema SHALL generar con `make notebooks` un notebook `.ipynb` por cada script `.py` de `notebooks/`, con las mismas celdas que el script. Los `.ipynb` generados MUST NOT versionarse. Implementa RF-06.

#### Scenario: Generar los notebooks

- **WHEN** se ejecuta `make notebooks` con el entorno instalado
- **THEN** existe junto a cada `notebooks/<nombre>.py` un `notebooks/<nombre>.ipynb` con sus celdas de código y de texto

#### Scenario: Los notebooks generados no se versionan

- **WHEN** se ejecuta `make notebooks` y después `git status`
- **THEN** ningún `.ipynb` aparece como archivo nuevo o modificado

#### Scenario: Regenerar tras editar el script

- **WHEN** se edita un `notebooks/*.py` y se vuelve a ejecutar `make notebooks`
- **THEN** el `.ipynb` correspondiente refleja el contenido actual del script

### Requirement: Notebook de inicio rápido con un detector preentrenado

El sistema SHALL ofrecer el notebook `01_quickstart`, que carga un detector YOLO preentrenado en COCO y muestra una imagen de ejemplo con sus detecciones (bounding box, clase y confianza), sin necesitar datos ni pesos propios del proyecto. Implementa RF-06.

#### Scenario: Ejecución de principio a fin

- **WHEN** se ejecutan todas las celdas del notebook `01_quickstart` generado, en un entorno recién instalado y con acceso a internet
- **THEN** termina sin errores y muestra la imagen de ejemplo con al menos una detección dibujada con su clase y su confianza

#### Scenario: Pesos preentrenados fuera del repositorio

- **WHEN** el notebook descarga los pesos preentrenados la primera vez
- **THEN** quedan en `models/` y no aparecen en `git status`, y las ejecuciones siguientes los reutilizan sin volver a descargarlos

### Requirement: Notebook de demo de punta a punta

El sistema SHALL ofrecer el notebook `03_demo`, que con los pesos entrenados del modelo de marcas recorre la demo completa: muestra una imagen con sus detecciones anotadas, analiza un vídeo de ejemplo y muestra el vídeo anotado reproducible dentro del notebook junto con algunos fotogramas con detecciones, y muestra el informe de exposición como una tabla con una fila por marca (detectada, segundos y porcentaje) y lo guarda en JSON en la carpeta de salidas. La imagen, el vídeo y el umbral de confianza MUST poder cambiarse en una única celda de parámetros al principio del notebook. Los vídeos de ejemplo MUST NOT versionarse. Implementa RF-06 y RF-05.

#### Scenario: Ejecución de principio a fin

- **WHEN** se ejecutan todas las celdas del notebook `03_demo` generado, con los pesos entrenados en `models/` y un vídeo de ejemplo en la carpeta de vídeos
- **THEN** termina sin errores, muestra la imagen anotada, el vídeo anotado reproducible, fotogramas con detecciones y la tabla del informe, y deja el JSON del informe en `outputs/`

#### Scenario: Cambiar el vídeo o el umbral

- **WHEN** se cambia el vídeo o el umbral en la celda de parámetros y se vuelve a ejecutar el notebook
- **THEN** el análisis, la tabla y el JSON corresponden al nuevo vídeo y umbral

#### Scenario: Falta el vídeo de ejemplo

- **WHEN** se ejecuta el notebook sin el vídeo indicado en la celda de parámetros
- **THEN** la celda del vídeo falla con un mensaje que indica la ruta esperada
