# PROJECT

> Por qué existe el producto, para quién y hasta dónde llega. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

- **Nombre:** AI Computer Vision — detector de logos en vídeo
- **Responsable:** Victor Gonzalez
- **Estado del documento:** Borrador

## 1. Resumen

Prueba de concepto que detecta logos de marcas en vídeos y genera un informe con el tiempo y el porcentaje de aparición de cada marca. Está pensada para una agencia de publicidad que quiere saber cuánta exposición en pantalla consiguen las marcas que representa. Se entrena reentrenando un detector de objetos preentrenado con un dataset público de logos. El proyecto tiene además un fin formativo: practicar el procesado de imágenes y la detección de objetos.

## 2. Problema y oportunidad

- **Problema:** medir a mano cuánto tiempo aparece un logo en un vídeo es lento y poco fiable.
- **Oportunidad:** automatizar esa medición permite comparar la exposición de cada marca y decidir dónde dirigir la inversión publicitaria.

## 3. Usuarios y partes interesadas

- **Usuarios:** analistas de la agencia que suben un vídeo y necesitan un informe de exposición por marca.
- **Partes interesadas:** la agencia (cliente del briefing) y el equipo evaluador, que revisa el repositorio, la demo en vivo, la presentación técnica y el tablero Kanban.

## 4. Objetivos y criterios de éxito

| ID | Objetivo | Cómo se comprueba |
|---|---|---|
| OBJ-1 | Detectar y localizar los logos de las marcas elegidas en una imagen | El modelo dibuja un bounding box con el nombre de la marca sobre imágenes de test y se reportan sus métricas de validación (mAP) |
| OBJ-2 | Analizar un vídeo completo y medir la exposición de cada marca | Dado un vídeo, se obtienen el vídeo anotado y un informe con el tiempo (s) y el porcentaje de duración en que aparece cada marca |
| OBJ-3 | Aplicar las técnicas de visión por computador que pide la evaluación | El repositorio documenta y usa preprocesamiento (resizing, normalización), aumento de datos (flip, crop, color jitter) y reentrenamiento de un modelo preentrenado |
| OBJ-4 | Entregar un proyecto reproducible y bien gestionado | El proyecto se ejecuta con Docker siguiendo el README, con ramas y commits limpios y un tablero Kanban en GitHub |

## 5. Principios de decisión

1. Llegar a la entrega a tiempo antes que añadir funcionalidad: primero el nivel esencial, luego el medio.
2. Reutilizar modelos, datasets y herramientas existentes antes que construir desde cero.
3. Que la demo funcione de forma fiable antes que maximizar la precisión del modelo.

## 6. Alcance

### Incluido

- Detección de tres marcas: Coca-Cola, Pepsi y Adidas (DEC-01, DEC-02).
- Entrenamiento a partir de un modelo de detección preentrenado, con preprocesamiento y aumento de datos.
- Detección en imágenes con bounding box, el nombre de la marca debajo y el porcentaje de confianza (niveles esencial y medio, más la confianza del avanzado; DEC-04).
- Análisis de archivos de vídeo: vídeo de salida anotado e informe con el tiempo y el porcentaje de aparición de cada marca.
- Ejecución en Docker.
- Presentación en notebooks `.ipynb` generados desde scripts `.py` (DEC-05).
- Repositorio documentado (README y código) y gestión del proyecto con Kanban en GitHub.

### Fuera de alcance

- Front web para subir vídeos y ver resultados (nivel experto): no cabe en el plazo.
- Servir el modelo en cloud y exponerlo como API (nivel experto): no cabe en el plazo.
- Procesado en tiempo real: el briefing no lo exige.

### Futuro

- Guardar las detecciones en una base de datos con el nombre del vídeo y los recortes de los bounding boxes (nivel avanzado).
- Ampliar la lista de marcas.
- Front web y API en cloud (nivel experto).

## 7. Restricciones, supuestos y riesgos

- **Restricciones:** entrega el 2026-11-04 a las 12:00; Python como lenguaje principal; Docker como entorno de ejecución; entregables fijados por el briefing (repositorio, demo en vivo, presentación técnica y Kanban).
- **Supuestos:** el dataset público OpenLogo contiene suficientes imágenes anotadas de las tres marcas para entrenar un modelo útil; hay acceso a una GPU (local o gratuita en la nube) para entrenar en un tiempo razonable.
- **Riesgos:**
  - Pocas imágenes por marca (~70 en FlickrLogos-32) → aumento de datos y, si hace falta, completar con un dataset de Roboflow Universe.
  - Los logos de los vídeos reales (pequeños, desenfocados, en movimiento) difieren de las fotos de entrenamiento → elegir vídeos de demo representativos y validar pronto con vídeo.
  - Plazo de menos de un día → priorizar el camino mínimo imagen → vídeo → informe y recortar lo demás.

## 8. Decisiones de producto

| ID | Decisión | Motivo | Estado |
|---|---|---|---|
| DEC-01 | Las marcas de la prueba de concepto son Coca-Cola, Pepsi y Adidas | Logos muy reconocibles y distintos entre sí, presentes en datasets públicos y fáciles de encontrar en vídeos | Aceptada |
| DEC-02 | El dataset de partida es OpenLogo (incluye FlickrLogos-32) | Descarga inmediata con bounding boxes de las marcas elegidas, sin registro. Su licencia de investigación es válida porque el proyecto es pedagógico, no comercial | Aceptada |
| DEC-03 | El alcance llega a los niveles esencial y medio del briefing, con Docker; el avanzado y el experto quedan para el futuro, salvo DEC-04 | Plazo de entrega corto | Aceptada |
| DEC-04 | Se muestra el porcentaje de confianza junto al nombre de la marca | El detector ya lo proporciona y cuesta muy poco | Aceptada |
| DEC-05 | La demo y la presentación se hacen en notebooks `.ipynb`; el trabajo se hace en `.py` con jupytext y los `.ipynb` se generan con `make` y no se versionan | Notebooks para presentar, `.py` para revisar diffs y mantener el código | Aceptada |

## 9. Preguntas abiertas

- ¿Quién forma el equipo (el briefing habla de dos personas)? Bloquea: el reparto de historias.
