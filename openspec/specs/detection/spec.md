# detection Specification

## Purpose

Detectar las marcas de la prueba de concepto en una imagen y devolverla anotada con el bounding box, la marca y la confianza de cada logo, para que una persona vea de un vistazo qué marcas aparecen (RF-03, RD-04).

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
