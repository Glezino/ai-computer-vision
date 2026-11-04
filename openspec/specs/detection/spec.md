# detection Specification

## Purpose

Detectar las marcas de la prueba de concepto en imágenes y vídeos y devolverlos anotados con el bounding box, la marca y la confianza de cada logo, para que una persona vea de un vistazo qué marcas aparecen, y entregar las detecciones por fotograma que necesita el informe de exposición (RF-03, RF-04, RNF-02, RD-04).

## Requirements

### Requirement: Imagen anotada con marca y confianza

El sistema SHALL detectar, en una imagen dada como archivo o como matriz de píxeles, los logos de las marcas del modelo entrenado y devolver una copia de la imagen en la que cada detección que alcance el umbral está enmarcada en un bounding box, con el nombre de la marca y su confianza en porcentaje entero (por ejemplo, `pepsi 87 %`) debajo del recuadro. Si no cabe debajo, la etiqueta MUST quedar dentro de los límites de la imagen. La imagen original MUST NOT modificarse. Junto a la imagen anotada, el sistema MUST devolver la lista de detecciones, cada una con su marca, su confianza en [0, 1] y su bounding box en píxeles. Implementa RF-03.

#### Scenario: Imagen con un logo

- **WHEN** se procesa una imagen con un logo de Pepsi que el modelo detecta con confianza 0,87
- **THEN** la imagen devuelta tiene un recuadro alrededor del logo con la etiqueta `pepsi 87 %` debajo, y la lista de detecciones contiene esa detección con su marca, confianza y caja

#### Scenario: Logo en el borde inferior

- **WHEN** una detección llega hasta el borde inferior de la imagen
- **THEN** su etiqueta se dibuja completa dentro de la imagen

#### Scenario: Imagen sin logos

- **WHEN** se procesa una imagen en la que el modelo no detecta ninguna marca por encima del umbral
- **THEN** se devuelve una imagen idéntica a la original, sin anotaciones, y una lista de detecciones vacía, sin error

### Requirement: Umbral de confianza configurable

Solo SHALL anotarse y devolverse las detecciones con confianza igual o superior al umbral. El umbral MUST ser del 50 % por defecto y MUST poder ajustarse en cada detección; un umbral fuera de [0, 1] MUST producir un error con un mensaje claro. Implementa RD-04.

#### Scenario: Umbral por defecto

- **WHEN** el modelo propone detecciones con confianza 0,70 y 0,30 y no se indica umbral
- **THEN** solo se anota y devuelve la de 0,70

#### Scenario: Umbral ajustado

- **WHEN** se detecta con un umbral del 80 % y el modelo propone una detección con confianza 0,70
- **THEN** la detección no se anota ni se devuelve

#### Scenario: Umbral no válido

- **WHEN** se detecta con un umbral de 1,5
- **THEN** se produce un error que indica que el umbral debe estar entre 0 y 1

### Requirement: Errores de entrada claros

Si el archivo de pesos del modelo no existe, el sistema SHALL producir un error que indique la ruta esperada y cómo obtener los pesos. Si la imagen indicada no existe o no se puede leer como imagen, el sistema SHALL producir un error que indique la ruta.

#### Scenario: Faltan los pesos

- **WHEN** se carga el modelo y no existe `models/brands.pt`
- **THEN** se produce un error que indica esa ruta y remite a las instrucciones de entrenamiento del README

#### Scenario: Imagen no legible

- **WHEN** se procesa una ruta que no existe o un archivo que no es una imagen
- **THEN** se produce un error que indica la ruta

### Requirement: Vídeo anotado con las detecciones de cada fotograma

El sistema SHALL procesar un archivo de vídeo fotograma a fotograma y generar un vídeo anotado en el que cada fotograma lleva sus detecciones dibujadas como en una imagen (bounding box, y debajo la marca y la confianza en porcentaje), con el mismo umbral configurable, del 50 % por defecto. El vídeo anotado MUST conservar la resolución, los fotogramas por segundo y el número de fotogramas del original, y por tanto su duración. Por defecto se guarda en la carpeta de salidas con el nombre del vídeo seguido de `_annotated`. Junto a la ruta del vídeo anotado, el sistema MUST devolver los fotogramas por segundo y, por cada fotograma, la lista de sus detecciones (marca, confianza y bounding box), utilizable directamente para el informe de exposición. Implementa RF-04.

#### Scenario: Vídeo con logos

- **WHEN** se analiza un vídeo de 50 fotogramas a 25 fps y 320×240 en el que el modelo detecta Pepsi en los 10 primeros
- **THEN** se genera un vídeo anotado de 50 fotogramas a 25 fps y 320×240 con las detecciones dibujadas en esos 10 fotogramas, y se devuelven 25 fps y 50 listas de detecciones, las 10 primeras con Pepsi

#### Scenario: Vídeo sin logos

- **WHEN** se analiza un vídeo en el que el modelo no detecta ninguna marca por encima del umbral
- **THEN** se genera el vídeo anotado sin anotaciones y todas las listas de detecciones están vacías, sin error

#### Scenario: Detecciones para el informe

- **WHEN** se genera el informe de exposición con el nombre del vídeo, las detecciones por fotograma y los fps devueltos por el análisis
- **THEN** el informe se calcula sin transformar las detecciones

### Requirement: Error claro con un vídeo no válido

Si el archivo indicado no existe, no se puede abrir como vídeo o no contiene fotogramas legibles, el sistema SHALL producir un error que indique la ruta, sin generar un vídeo anotado. Implementa RF-04.

#### Scenario: Archivo que no es un vídeo

- **WHEN** se analiza un archivo de texto con extensión `.mp4`
- **THEN** se produce un error que indica la ruta y no se crea el vídeo anotado

#### Scenario: Archivo inexistente

- **WHEN** se analiza una ruta que no existe
- **THEN** se produce un error que indica la ruta

### Requirement: Tiempo de procesado apto para una demo

El análisis de un vídeo de 1 minuto SHALL completarse en menos de 5 minutos en el equipo de la demo, con el modelo de marcas y en CPU. El sistema MUST devolver el tiempo de procesado para poder comprobarlo. Implementa RNF-02.

#### Scenario: Vídeo de 1 minuto

- **WHEN** se analiza un vídeo de 1 minuto con el modelo de marcas en el equipo de la demo
- **THEN** el análisis termina en menos de 5 minutos y devuelve el tiempo empleado

### Requirement: Vista previa web del vídeo anotado

El sistema SHALL generar, a partir de un vídeo anotado, una vista previa en un formato que los navegadores reproducen (WebM), con los mismos fotogramas y fotogramas por segundo, y reducida a un ancho máximo configurable sin cambiar la proporción; un vídeo más estrecho que ese ancho conserva su tamaño. Por defecto se guarda junto al vídeo anotado con el mismo nombre y extensión `.webm`. Implementa RF-04 y RF-06.

#### Scenario: Vídeo ancho

- **WHEN** se genera la vista previa de un vídeo de 50 fotogramas a 25 fps y 1280×720 con un ancho máximo de 640
- **THEN** se crea un `.webm` de 50 fotogramas a 25 fps y 640×360

#### Scenario: Vídeo estrecho

- **WHEN** se genera la vista previa de un vídeo de 320×240 con un ancho máximo de 640
- **THEN** el `.webm` mantiene 320×240

#### Scenario: Vídeo no válido

- **WHEN** se genera la vista previa de un archivo que no es un vídeo
- **THEN** se produce un error que indica la ruta
