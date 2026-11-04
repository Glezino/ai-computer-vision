## 1. Filtrado y dibujo (TDD)

- [x] 1.1 Escribir en `tests/test_detection.py` los tests de `select_detections` con un resultado falso (umbral por defecto, ajustado y en el límite 0,50) y de la validación del umbral fuera de [0, 1]; verificar que fallan porque `detection` no existe
- [x] 1.2 Implementar en `src/logo_detector/detection.py` `BrandBox` y `select_detections`; verificar que los tests de 1.1 pasan con `make test`
- [x] 1.3 Escribir los tests de `draw_detections` (sin detecciones devuelve una copia idéntica, etiqueta `pepsi 87 %`, píxeles cambiados bajo la caja, etiqueta dentro de la imagen en el borde inferior y la original sin modificar) e implementarlo; verificar con `make test`

## 2. Detección en imagen

- [x] 2.1 Implementar `load_model` y `detect_image` (ruta o matriz BGR, `ImageDetection`) con los errores de pesos inexistentes e imagen no legible, y sus tests sin modelo; verificar con `make test` y `make lint`
- [x] 2.2 Añadir el test de integración con `models/brands.pt` sobre una imagen de `data/openlogo/images/test` que se salta si faltan los pesos o la imagen; verificar que pasa en local y que se salta sin ellos

## 3. Documentación

- [x] 3.1 Actualizar ARCHITECTURE §3 (`detection` «Actual» para imagen, vídeo pendiente de #13) y §8 (tests de `detection`); verificar que no duplica lo que dice la spec
