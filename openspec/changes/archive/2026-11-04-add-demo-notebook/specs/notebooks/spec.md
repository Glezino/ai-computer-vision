## ADDED Requirements

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
