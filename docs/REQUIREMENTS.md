# REQUIREMENTS

> Qué debe hacer el producto: requisitos con ID estable y criterios de aceptación de producto. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

## 1. Glosario

| Término | Definición |
|---|---|
| Marca | Clase que el modelo detecta: Coca-Cola, Pepsi o Adidas ([PROJECT DEC-01](PROJECT.md#8-decisiones-de-producto)) |
| Detección | Aparición de una marca en un fotograma: bounding box, marca y confianza |
| Confianza | Probabilidad (0-100 %) que el modelo asigna a una detección |
| Umbral de confianza | Confianza mínima para aceptar una detección |
| Exposición | Tiempo, en segundos, en que una marca aparece en un vídeo, y su porcentaje sobre la duración total |
| Informe | Resumen de un vídeo con la exposición de cada marca |

## 2. Flujos principales

1. Desarrollador → prepara el dataset y entrena el modelo → obtiene unos pesos y sus métricas de validación.
2. Analista → aplica el modelo a una imagen → ve la imagen con los logos enmarcados, su marca y su confianza.
3. Analista → aplica el modelo a un vídeo → obtiene el vídeo anotado y el informe de exposición por marca.

## 3. Requisitos funcionales

### RF-01 — Dataset de entrenamiento preparado

- **Objetivo:** OBJ-1, OBJ-3
- **Ámbito:** Base

El sistema debe obtener las imágenes anotadas de las marcas a partir del dataset de partida y dejarlas listas para entrenar, divididas en entrenamiento, validación y test.

**Criterios de aceptación:**

- El dataset resultante solo contiene las tres marcas, con sus bounding boxes.
- Las particiones de entrenamiento, validación y test no comparten imágenes.
- Se informa del número de imágenes y de bounding boxes por marca y partición.

### RF-02 — Modelo de detección de marcas entrenado

- **Objetivo:** OBJ-1, OBJ-3
- **Ámbito:** Base

El sistema debe reentrenar un modelo de detección preentrenado para que detecte las tres marcas, aplicando preprocesamiento (redimensionado y normalización) y aumento de datos (flip, crop y color jitter).

**Criterios de aceptación:**

- El entrenamiento produce unos pesos reutilizables.
- Se reportan las métricas de validación (precisión, recall y mAP) global y por marca.
- La configuración de preprocesamiento y aumento de datos queda documentada y es reproducible.

### RF-03 — Detección en una imagen

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El sistema debe detectar las marcas en una imagen y devolverla con cada logo enmarcado en un bounding box, con el nombre de la marca debajo y su confianza en porcentaje.

**Criterios de aceptación:**

- Cada detección por encima del umbral muestra su bounding box, su marca y su confianza.
- Una imagen sin logos se devuelve sin anotaciones y sin error.

### RF-04 — Análisis de un vídeo

- **Objetivo:** OBJ-2
- **Ámbito:** Base

El sistema debe procesar un archivo de vídeo y generar un vídeo anotado con las detecciones de cada fotograma, como en RF-03.

**Criterios de aceptación:**

- El vídeo anotado conserva la duración y la resolución del original.
- Un archivo que no es un vídeo válido produce un mensaje de error claro.

### RF-05 — Informe de exposición

- **Objetivo:** OBJ-2
- **Ámbito:** Base

El sistema debe generar, para cada vídeo analizado, un informe que indique si se ha detectado cada marca, el tiempo en segundos en que aparece y el porcentaje de la duración del vídeo que supone.

**Criterios de aceptación:**

- El informe incluye el nombre del vídeo, su duración y una fila por marca, también para las no detectadas (0 s, 0 %).
- El informe se muestra en el notebook y se guarda en un archivo legible por máquina.

### RF-06 — Notebooks de demo y presentación

- **Objetivo:** OBJ-4
- **Ámbito:** Base

El sistema debe ofrecer notebooks que recorran el entrenamiento, la detección en imagen y el análisis de vídeo, generados desde scripts `.py` ([PROJECT DEC-05](PROJECT.md#8-decisiones-de-producto)).

**Criterios de aceptación:**

- Un único comando genera los `.ipynb` a partir de los `.py`.
- Los notebooks se ejecutan de principio a fin con los pesos entrenados y los vídeos de ejemplo.

## 4. Requisitos no funcionales

### RNF-01 — Reproducibilidad con Docker

El proyecto debe poder ejecutarse en un contenedor Docker siguiendo el README, sin instalar dependencias en el equipo.

**Criterios de aceptación:**

- Con Docker instalado, los comandos del README levantan el entorno y ejecutan la detección sobre un ejemplo.

### RNF-02 — Tiempo de procesado de vídeo

No se exige tiempo real, pero un vídeo de demo de hasta 1 minuto debe procesarse en un tiempo apto para una demo en vivo.

**Criterios de aceptación:**

- Un vídeo de 1 minuto se procesa en menos de 5 minutos en el equipo de la demo.

### RNF-03 — Calidad mínima del modelo

El modelo debe ser lo bastante preciso para que la demo sea convincente.

**Criterios de aceptación:**

- mAP@0.5 de validación ≥ 0,6 en el conjunto de las tres marcas.

## 5. Reglas de dominio

- **RD-01:** Una marca cuenta como presente en un fotograma si tiene al menos una detección con confianza igual o superior al umbral.
- **RD-02:** El tiempo de exposición de una marca es el número de fotogramas en que está presente dividido entre los fotogramas por segundo del vídeo; varios logos de la misma marca en un fotograma cuentan una sola vez.
- **RD-03:** El porcentaje de exposición es el tiempo de exposición dividido entre la duración del vídeo, por 100.
- **RD-04:** El umbral de confianza por defecto es 50 % y se puede ajustar.
