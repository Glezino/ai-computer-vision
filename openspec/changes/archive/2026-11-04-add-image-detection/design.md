## Context

- `config.py` ya define `MODELS_DIR`, `BRAND_MODEL = "brands.pt"`, `CONFIDENCE_THRESHOLD = 0.5`, `IMAGE_SIZE = 640` y `BRANDS`. Los nombres de clase de `brands.pt` son `{0: "coca-cola", 1: "pepsi", 2: "adidas"}` (comprobado), los de `config.BRANDS`.
- `notebooks/01_quickstart.py` usa `result.plot()` de Ultralytics, que pone la etiqueta **encima** de la caja y la confianza como `0.87`; RF-03 pide la marca **debajo** y la confianza en porcentaje.
- `report.Detection(brand, confidence)` es la entrada de `report`; ARCHITECTURE §5 prevé que `detection` produzca detecciones por fotograma para el vídeo (#13).
- `training.py` carga los modelos con `YOLO(ruta)`.

Motivación en `proposal.md`; comportamiento en `specs/detection/spec.md`.

## Goals / Non-Goals

**Goals:**

- Separar la inferencia (Ultralytics) del filtrado y el dibujo, para probar estos sin modelo.
- Dejar una función por imagen que #13 pueda llamar fotograma a fotograma sin cambios.

**Non-Goals:**

- Leer o escribir vídeo, y convertir a `report.Detection` (#13).
- Guardar la imagen anotada en disco o mostrarla: lo hace quien llama (notebook).

## Decisions

- **API** en `src/logo_detector/detection.py`:
  - `BrandBox(NamedTuple)`: `brand: str`, `confidence: float` en [0, 1] y `box: tuple[int, int, int, int]` (`x1, y1, x2, y2` en píxeles). Tiene los campos de `report.Detection` más la caja; no se reutiliza ese tipo porque `report` no necesita la caja, y extenderlo cambiaría su interfaz. #13 convierte con `Detection(b.brand, b.confidence)`.
  - `load_model(weights: Path = config.MODELS_DIR / config.BRAND_MODEL) -> YOLO`: si el archivo no existe, `FileNotFoundError` con la ruta y la indicación de entrenar con `02_training` (README).
  - `detect_image(model, image: str | Path | np.ndarray, threshold=config.CONFIDENCE_THRESHOLD) -> ImageDetection`, con `ImageDetection(NamedTuple)`: `image: np.ndarray` (BGR anotada) y `detections: list[BrandBox]`.
  - `draw_detections(image, detections) -> np.ndarray`: función pura que devuelve una copia anotada; sin detecciones, una copia idéntica.
- **Entrada.** Se acepta ruta o matriz BGR (la de OpenCV), porque #13 pasará fotogramas de `cv2.VideoCapture`. Una ruta se lee con `cv2.imread`; si devuelve `None` (no existe o no es imagen), `ValueError` con la ruta. Se descarta pasar la ruta directamente a Ultralytics: su error no es claro y obligaría a releer la imagen para dibujarla.
- **Umbral.** `ValueError` si está fuera de [0, 1]. Se llama a `model.predict(image, conf=threshold, imgsz=config.IMAGE_SIZE, verbose=False)` y después se filtra `confidence >= threshold` con una función pura (`select_detections`) que convierte el resultado en `BrandBox`. El filtro propio garantiza el «igual o superior» de la spec (coherente con RD-01) aunque Ultralytics use `>` internamente, y permite probar el umbral sin modelo.
- **Dibujo** con OpenCV (`cv2.rectangle`, `cv2.putText`, `cv2.getTextSize`):
  - etiqueta `f"{brand} {round(confidence * 100)} %"` (espacio antes de `%`, norma del español), sobre un rectángulo relleno del color de la caja y texto blanco o negro según contraste;
  - posición: justo debajo de `y2`; si no cabe, se sube hasta que el fondo de la etiqueta coincide con el borde inferior de la imagen, y en horizontal se recorta para no salirse;
  - un color fijo por marca (índice en `config.BRANDS`), para que la misma marca se vea igual en todas las imágenes y fotogramas; grosor de línea y tamaño de fuente proporcionales al tamaño de la imagen, con mínimo.
  - Alternativa descartada: `result.plot()` con `labels=False` más etiqueta propia; mezcla dos estilos y no simplifica.
- **Tests** (`tests/test_detection.py`):
  - unitarios, con TDD: `draw_detections` (sin detecciones la copia es idéntica; con una, cambian los píxeles bajo la caja; borde inferior dentro de la imagen; la original no se modifica), formato de la etiqueta, `select_detections` con un resultado falso (umbral por defecto, ajustado y en el límite) y validación del umbral;
  - errores: `load_model` con ruta inexistente y `detect_image` con ruta inexistente o archivo que no es imagen (no necesitan pesos);
  - integración con `brands.pt` sobre una imagen de test de `data/openlogo/images/test`, marcada `@pytest.mark.skipif` si faltan los pesos o la imagen; comprueba que hay al menos una detección de la marca esperada y que la imagen anotada difiere de la original. No corre en el CI (ARCHITECTURE §8).

## Risks / Trade-offs

- [Etiquetas superpuestas si hay logos muy juntos] → se acepta en la prueba de concepto; no lo exige RF-03.
- [El test de integración depende de pesos y datos locales no versionados] → se salta con un motivo explícito; la lógica propia queda cubierta por los unitarios.
- [Las predicciones cambian si se reentrena el modelo] → el test de integración solo exige una detección de la marca esperada, no confianzas exactas.
