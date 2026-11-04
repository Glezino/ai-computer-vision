## Context

- `detection.py` (#12) ya tiene `detect_image(model, image, threshold)`, que acepta una matriz BGR y devuelve `ImageDetection(image, detections)`, y `BrandBox(brand, confidence, box)`.
- `report.build_report(video, frames, fps, threshold, brands)` (#11) solo lee `.brand` y `.confidence` de cada detección. `BrandBox` es una `NamedTuple` con esos dos campos, así que una lista de `list[BrandBox]` por fotograma le sirve sin conversión.
- OpenCV 5.0 (`opencv-python`) lee y escribe vídeo; el paquete de pip no incluye H.264, pero sí el códec `mp4v` (MPEG-4 Part 2) en contenedor `.mp4`.
- Inferencia medida en #10: ~28 ms por imagen de 640 px en CPU (Ryzen 5 5600). Un minuto a 30 fps son 1800 fotogramas: ~50 s de inferencia más lectura, dibujo y escritura.

Motivación en `proposal.md`; comportamiento en `specs/detection/spec.md`.

## Goals / Non-Goals

**Goals:**

- Reutilizar la detección por imagen sin duplicar lógica.
- Probar el bucle de vídeo en el CI sin pesos ni vídeos versionados.

**Non-Goals:**

- Barra de progreso o vista previa en el notebook (#14).
- Conservar el audio: OpenCV no lo gestiona y el informe no lo necesita.
- Saltar fotogramas para acelerar: cambiaría el informe y RNF-02 se cumple sin ello.

## Decisions

- **API** en `detection.py`:
  - `analyze_video(model, video, output=None, threshold=config.CONFIDENCE_THRESHOLD) -> VideoAnalysis`;
  - `VideoAnalysis(NamedTuple)`: `output: Path`, `fps: float`, `frames: list[list[BrandBox]]` y `elapsed_s: float`;
  - salida por defecto: `config.OUTPUTS_DIR / f"{Path(video).stem}_annotated.mp4"`, creando la carpeta.

  Uso previsto por la demo: `report.build_report(Path(video).name, analysis.frames, analysis.fps)`. Se descarta convertir a `report.Detection` dentro de `detection`: añadiría una dependencia de `detection` hacia `report` para nada, porque `BrandBox` ya cumple lo que `report` lee. Un test lo comprueba para que no se rompa sin avisar.
- **Bucle:** `cv2.VideoCapture` lee cada fotograma, `detect_image(model, frame, threshold)` lo detecta y lo anota, y `cv2.VideoWriter` lo escribe. Se escriben todos los fotogramas, con o sin detecciones, para conservar duración y número de fotogramas. Se valida el umbral antes de abrir nada.
- **Escritura:** `VideoWriter` con `fourcc` `mp4v`, los fps de `CAP_PROP_FPS` y el tamaño del primer fotograma leído (no el de `CAP_PROP_FRAME_*`, que algunos contenedores informan mal). El writer se abre tras leer el primer fotograma y se libera en un `finally`, igual que el capture.
- **Validación**, con `ValueError` que indica la ruta:
  - el archivo no existe, `VideoCapture` no lo abre o el primer `read()` falla;
  - `CAP_PROP_FPS` es 0 o no es finito: sin fps no hay duración ni informe.

  Si falla después de crear el writer, se borra el vídeo parcial para no dejar un resultado engañoso.
- **Tiempo:** `time.perf_counter()` alrededor del bucle; `elapsed_s` en el resultado y un `logging.info` con fotogramas, segundos y fotogramas por segundo procesados (ARCHITECTURE §8, logs en consola).
- **Tests** (`tests/test_detection.py`):
  - un *fixture* genera con `cv2.VideoWriter` un vídeo `mp4v` de 50 fotogramas a 25 fps y 320×240 en `tmp_path`, y se usa el `FakeModel` de #12 con resultados por llamada (Pepsi en los 10 primeros);
  - se comprueban número de fotogramas, fps y tamaño del vídeo anotado leyéndolo con `VideoCapture`, las 50 listas de detecciones, que los fotogramas con detección difieren del original, la ruta por defecto, el vídeo sin logos y que `build_report` acepta el resultado;
  - errores: archivo de texto con extensión `.mp4` (sin vídeo de salida), ruta inexistente y umbral no válido.
- **Medición RNF-02:** no es un test automático (depende del equipo y de pesos no versionados). Se genera un vídeo de 1 minuto a 30 fps y 1280×720 con imágenes de test del dataset en `outputs/`, se analiza con `brands.pt` y el tiempo se documenta en ARCHITECTURE §8. Si la persona aporta un vídeo real de la demo, se mide también con él.

## Risks / Trade-offs

- [`mp4v` no se reproduce en el navegador, así que no se puede incrustar en el notebook tal cual] → se reproduce en cualquier reproductor de escritorio (VLC, Películas y TV). Cómo mostrarlo en la demo se decide en #14 (fotogramas de muestra o recodificar).
- [Vídeos con fps variable] → se usan los fps medios que da el contenedor; la duración puede diferir unas centésimas. Aceptable para la prueba de concepto.
- [Vídeos de alta resolución (4K) más lentos al leer y escribir] → la inferencia se hace a 640 px igualmente; si superan RNF-02, la demo usará 1080p o menos.
