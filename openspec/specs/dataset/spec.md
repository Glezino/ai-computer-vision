# dataset Specification

## Purpose

Preparar, a partir de OpenLogo, el dataset de las tres marcas de la prueba de concepto en formato YOLO y dividido en particiones, listo para entrenar el detector (RF-01, PROJECT DEC-01 y DEC-02).

## Requirements

### Requirement: Dataset con solo las tres marcas

El sistema SHALL generar con `make data` un dataset en `data/` cuyas únicas clases son Coca-Cola, Pepsi y Adidas, con un bounding box por cada logo anotado de esas marcas en OpenLogo. Cada etiqueta de OpenLogo que corresponde a una variante de una marca (logo gráfico o texto) MUST asignarse a la clase de esa marca: `cocacola` y `coke` → Coca-Cola; `pepsi`, `pepsi_text` y `pepsi_text1` → Pepsi; `adidas`, `adidas1` y `adidas_text` → Adidas. Implementa RF-01.

#### Scenario: Solo imágenes con alguna marca

- **WHEN** se ejecuta `make data`
- **THEN** cada imagen del dataset tiene al menos un bounding box de Coca-Cola, Pepsi o Adidas, y ninguna imagen de OpenLogo sin esas marcas forma parte del dataset

#### Scenario: Variantes agrupadas por marca

- **WHEN** una imagen de OpenLogo tiene logos anotados como `adidas1` y `adidas_text`
- **THEN** en el dataset sus dos bounding boxes tienen la clase Adidas

#### Scenario: Otros logos descartados

- **WHEN** una imagen contiene una de las tres marcas y además logos de otras marcas
- **THEN** la imagen se incluye solo con los bounding boxes de las tres marcas

#### Scenario: Formato listo para entrenar

- **WHEN** termina `make data`
- **THEN** el dataset incluye un `data.yaml` con las tres clases y las rutas de cada partición, y cada imagen tiene su archivo de etiquetas YOLO con coordenadas normalizadas entre 0 y 1

### Requirement: Particiones sin solapes y reproducibles

El sistema SHALL dividir el dataset en entrenamiento, validación y test en proporción aproximada 70/15/15, manteniendo esa proporción en cada marca. Ninguna imagen MUST aparecer en más de una partición, ni siquiera como copia con otro nombre. La división MUST ser la misma en cada ejecución con la misma semilla. Implementa RF-01.

#### Scenario: Particiones disjuntas

- **WHEN** termina `make data`
- **THEN** ninguna imagen, ni otra con idéntico contenido, aparece en dos particiones

#### Scenario: Proporciones por marca

- **WHEN** termina `make data`
- **THEN** para cada marca, sus imágenes se reparten en torno al 70 %, 15 % y 15 % entre entrenamiento, validación y test

#### Scenario: Ejecución repetida

- **WHEN** se ejecuta `make data` dos veces con la misma configuración
- **THEN** cada imagen queda en la misma partición en ambas ejecuciones

### Requirement: Estadísticas del dataset

El sistema SHALL informar, al terminar la preparación, del número de imágenes y de bounding boxes por marca y partición. Implementa RF-01.

#### Scenario: Resumen por marca y partición

- **WHEN** termina `make data`
- **THEN** se muestra una tabla con, para cada marca y cada partición (entrenamiento, validación y test), el número de imágenes que la contienen y el número de bounding boxes, además de los totales
