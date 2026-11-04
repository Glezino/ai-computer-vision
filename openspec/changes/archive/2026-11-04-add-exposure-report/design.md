## Context

- `config.py` ya define `BRANDS = ("coca-cola", "pepsi", "adidas")`, `CONFIDENCE_THRESHOLD = 0.5` y `OUTPUTS_DIR`, que no se versiona (`.gitignore`).
- ARCHITECTURE §3 y §5: `report` es lógica pura (detecciones → informe), sin dependencia del modelo; el notebook le pasa las detecciones por fotograma y los fps que devuelve `detection` (#13, aún sin implementar), muestra la tabla y guarda el JSON (#14).
- Los nombres de clase de `brands.pt` son los de `config.BRANDS`, porque el dataset se genera en ese orden.

Motivación en `proposal.md`; comportamiento en `specs/report/spec.md`.

## Goals / Non-Goals

**Goals:**

- Que `report` defina la forma mínima de entrada que necesita, para que #13 la produzca sin conocer el cálculo.
- Probar todas las reglas RD con datos construidos a mano, sin modelo ni vídeo.

**Non-Goals:**

- Formatear la tabla para el notebook o redondear valores para mostrarlos (#14).
- Leer un informe JSON de vuelta como objeto del dominio: no hay consumidor que lo necesite.

## Decisions

- **Entrada.** `build_report(video, frames, fps, threshold=config.CONFIDENCE_THRESHOLD, brands=config.BRANDS) -> ExposureReport`:
  - `video: str`, el nombre del vídeo tal como se mostrará (por ejemplo, `demo.mp4`);
  - `frames: Sequence[Sequence[Detection]]`, una lista por fotograma, vacía si no hay detecciones;
  - `Detection` es un `NamedTuple(brand: str, confidence: float)` definido en `report.py`, con la confianza en [0, 1] tal como la da Ultralytics.

  El número de fotogramas es `len(frames)`; así no se pasa un dato que pueda contradecir la lista. Se descarta un diccionario disperso `{fotograma: detecciones}` porque obliga a pasar aparte el número de fotogramas y lo puede desalinear. La posición, la caja y el índice de fotograma no se incluyen: el cálculo no los usa.
- **Dónde vive `Detection`.** En `report.py`, el consumidor, porque `detection` aún no existe. Si #13 necesita compartirlo con más usos, puede moverlo a otro módulo sin cambiar el comportamiento; en ese momento se decide si se registra como contrato en `docs/CONTRACTS/` (la regla es registrarlo cuando otro componente dependa de él).
- **Salida.** `ExposureReport` y `BrandExposure` son *dataclasses* congeladas:
  - `ExposureReport(video, duration_s, fps, frame_count, threshold, brands: tuple[BrandExposure, ...])`;
  - `BrandExposure(brand, detected, seconds, percentage)`, en el orden de `config.BRANDS`.

  Se guardan `fps`, `frame_count` y `threshold` para que el informe sea interpretable y reproducible por sí solo. Los valores no se redondean: el redondeo es de presentación.
- **Cálculo** (RD-01…RD-03): por cada fotograma, el conjunto de marcas con alguna detección `confidence >= threshold`; se cuentan los fotogramas por marca con un `Counter`. `seconds = count / fps`, `duration_s = frame_count / fps` y `percentage = seconds / duration_s * 100`, que equivale a `100 * count / frame_count`, y se calcula así para evitar el error de redondeo de dividir dos cocientes (multiplicar por 100 al final también lo introduce: `0.3 * 100` da `30.000000000000004`).
- **Validación**, con `ValueError` y mensaje en español:
  - `fps <= 0`, `frames` vacío o `threshold` fuera de [0, 1];
  - una detección cuya marca no está en `brands`: indica un modelo o una configuración que no corresponden, y descartarla en silencio falsearía el informe.
- **JSON.** `save_report(report, path=None) -> Path`:
  - por defecto, `OUTPUTS_DIR / f"{Path(video).stem}_report.json"`; crea la carpeta si falta;
  - contenido: `dataclasses.asdict(report)` con `json.dumps(indent=2, ensure_ascii=False)`, en UTF-8; las filas quedan como lista de objetos;
  - devuelve la ruta escrita, para que el notebook la muestre.

  Ejemplo:

  ```json
  {
    "video": "demo.mp4",
    "duration_s": 4.0,
    "fps": 25.0,
    "frame_count": 100,
    "threshold": 0.5,
    "brands": [
      {"brand": "coca-cola", "detected": false, "seconds": 0.0, "percentage": 0.0},
      {"brand": "pepsi", "detected": true, "seconds": 1.2, "percentage": 30.0},
      {"brand": "adidas", "detected": false, "seconds": 0.0, "percentage": 0.0}
    ]
  }
  ```
- **Tests** (`tests/test_report.py`, TDD): un caso por escenario de la spec, con fotogramas construidos con un *helper*; el guardado usa `tmp_path`, también para la ruta por defecto (con `monkeypatch` de `config.OUTPUTS_DIR`).

## Risks / Trade-offs

- [#13 entrega las detecciones en otra forma] → La forma es mínima (marca y confianza por fotograma) y se convierte en una línea desde los resultados de Ultralytics; si #13 propone otra, se ajusta con un `update` de este diseño o del suyo.
- [El fps real de algunos vídeos es variable] → Se usa el fps nominal que da OpenCV; la duración puede diferir unas centésimas de la del reproductor. Suficiente para la prueba de concepto.
- [Informes grandes de vídeos largos] → El JSON solo tiene una fila por marca, no por fotograma; su tamaño no depende de la duración.
