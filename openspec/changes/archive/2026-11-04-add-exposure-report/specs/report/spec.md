## Purpose

Calcular, a partir de las detecciones por fotograma de un vídeo, cuánto tiempo y qué porcentaje de su duración aparece cada marca, y guardarlo en un archivo legible por máquina (RF-05, RD-01…RD-04).

## ADDED Requirements

### Requirement: Informe con una fila por marca

El sistema SHALL generar, a partir del nombre de un vídeo, sus detecciones por fotograma (marca y confianza) y sus fotogramas por segundo, un informe con el nombre del vídeo, su duración en segundos y una fila por cada marca de la prueba de concepto (Coca-Cola, Pepsi y Adidas). Cada fila MUST indicar si la marca se ha detectado, su tiempo de exposición en segundos y su porcentaje de exposición. Las marcas no detectadas MUST aparecer con 0 s y 0 %. La duración del vídeo es el número de fotogramas dividido entre los fotogramas por segundo. Implementa RF-05.

#### Scenario: Marca detectada y marcas no detectadas

- **WHEN** se genera el informe de un vídeo de 100 fotogramas a 25 fps en el que solo aparece Pepsi
- **THEN** el informe indica el nombre del vídeo y una duración de 4 s, y tiene exactamente tres filas: Pepsi como detectada, y Coca-Cola y Adidas como no detectadas con 0 s y 0 %

#### Scenario: Vídeo sin detecciones

- **WHEN** se genera el informe de un vídeo en el que ningún fotograma tiene detecciones
- **THEN** las tres marcas aparecen como no detectadas con 0 s y 0 %

### Requirement: Presencia por umbral de confianza

Una marca SHALL contar como presente en un fotograma solo si tiene en él al menos una detección con confianza igual o superior al umbral. El umbral MUST ser del 50 % por defecto y MUST poder ajustarse al generar el informe. Implementa RD-01 y RD-04.

#### Scenario: Confianza en el umbral

- **WHEN** un fotograma tiene una detección de Adidas con confianza 0,50 y el umbral es el de por defecto
- **THEN** Adidas cuenta como presente en ese fotograma

#### Scenario: Confianza por debajo del umbral

- **WHEN** un fotograma tiene una detección de Adidas con confianza 0,49 y el umbral es el de por defecto
- **THEN** Adidas no cuenta como presente en ese fotograma

#### Scenario: Umbral ajustado

- **WHEN** se genera el informe con un umbral del 80 % y una detección de Adidas tiene confianza 0,70
- **THEN** Adidas no cuenta como presente en ese fotograma

#### Scenario: Umbral fuera de rango

- **WHEN** se genera el informe con un umbral menor que 0 o mayor que 1
- **THEN** se produce un error con un mensaje claro y no se genera el informe

### Requirement: Tiempo y porcentaje de exposición

El tiempo de exposición de una marca SHALL ser el número de fotogramas en que está presente dividido entre los fotogramas por segundo del vídeo; varias detecciones de la misma marca en un fotograma MUST contar como un solo fotograma. El porcentaje de exposición SHALL ser el tiempo de exposición dividido entre la duración del vídeo, por 100. Implementa RD-02 y RD-03.

#### Scenario: Cálculo de tiempo y porcentaje

- **WHEN** Coca-Cola está presente en 50 de los 100 fotogramas de un vídeo a 25 fps
- **THEN** su tiempo de exposición es 2 s y su porcentaje es 50 %

#### Scenario: Varios logos de una marca en un fotograma

- **WHEN** un fotograma tiene tres detecciones de Coca-Cola por encima del umbral
- **THEN** ese fotograma suma una sola vez al tiempo de Coca-Cola

#### Scenario: Varias marcas en un fotograma

- **WHEN** un fotograma tiene detecciones de Coca-Cola y de Pepsi por encima del umbral
- **THEN** ese fotograma suma al tiempo de las dos marcas

#### Scenario: Datos del vídeo no válidos

- **WHEN** se genera el informe con unos fotogramas por segundo menores o iguales que 0, o sin ningún fotograma
- **THEN** se produce un error con un mensaje claro y no se genera el informe

### Requirement: Informe guardado en JSON

El sistema SHALL guardar el informe en un archivo JSON con el nombre del vídeo, su duración, el umbral aplicado y las filas por marca. Por defecto MUST guardarse en `outputs/`, creando la carpeta si no existe, y la ruta MUST poder indicarse. Volver a cargar el archivo MUST dar los mismos datos del informe. Implementa RF-05.

#### Scenario: Guardado por defecto

- **WHEN** se guarda el informe del vídeo `demo.mp4` sin indicar ruta
- **THEN** se crea en `outputs/` un archivo JSON con el nombre del vídeo, su duración, el umbral y una fila por marca

#### Scenario: Ida y vuelta

- **WHEN** se carga como JSON un informe guardado
- **THEN** contiene los mismos valores que el informe generado
