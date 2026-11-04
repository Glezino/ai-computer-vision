## ADDED Requirements

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
