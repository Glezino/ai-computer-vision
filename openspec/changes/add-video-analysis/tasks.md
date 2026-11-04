## 1. Bucle de vídeo (TDD)

- [x] 1.1 Escribir en `tests/test_detection.py` el *fixture* del vídeo sintético y los tests de `analyze_video` con un modelo simulado (fotogramas, fps y tamaño del vídeo anotado, 50 listas de detecciones con Pepsi en las 10 primeras, fotogramas anotados distintos del original, ruta por defecto en `outputs/` y vídeo sin logos); verificar que fallan porque `analyze_video` no existe
- [x] 1.2 Implementar `VideoAnalysis` y `analyze_video` (lectura, detección con `detect_image`, escritura `mp4v` y tiempo); verificar que los tests de 1.1 pasan con `make test`
- [x] 1.3 Añadir el test de que `report.build_report` acepta las detecciones y los fps del análisis; verificar con `make test`

## 2. Archivos no válidos

- [x] 2.1 Escribir los tests de archivo de texto con extensión `.mp4` (error con la ruta y sin vídeo de salida), ruta inexistente y umbral no válido, e implementar la validación y el borrado del vídeo parcial; verificar con `make test` y `make lint`

## 3. Tiempo de procesado (RNF-02)

- [x] 3.1 Generar en `outputs/` un vídeo de 1 minuto a 30 fps y 1280×720 con imágenes de test del dataset, analizarlo con `brands.pt` y verificar que tarda menos de 5 minutos; si hay un vídeo real de la demo, medirlo también
- [x] 3.2 Comprobar el vídeo anotado real: misma duración y resolución que el original, y anotaciones visibles en un fotograma con logo

## 4. Documentación

- [x] 4.1 Actualizar ARCHITECTURE §3 (`detection` «Actual»), §5 (flujo de análisis de vídeo según lo implementado) y §8 (tests de vídeo y tiempo medido frente a RNF-02); verificar que no duplica lo que dice la spec
