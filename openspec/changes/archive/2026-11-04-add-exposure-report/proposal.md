## Why

Historia [#11](https://github.com/Glezino/ai-computer-vision/issues/11), la única de la épica E3 (#4). Para medir la exposición de cada marca en un vídeo (OBJ-2) hace falta convertir las detecciones por fotograma en tiempo y porcentaje de aparición. Implementa RF-05 y las reglas RD-01, RD-02, RD-03 y RD-04. No depende del modelo, así que puede hacerse ya y probarse con detecciones de ejemplo, en paralelo a la detección en vídeo (#13).

## What Changes

- Componente `report` (`src/logo_detector/report.py`), lógica pura sin dependencia del modelo:
  - a partir del nombre del vídeo, sus detecciones por fotograma (marca y confianza) y sus fps, calcula la duración del vídeo y, para cada marca, si se ha detectado, el tiempo de exposición en segundos y el porcentaje de la duración;
  - aplica un umbral de confianza, 50 % por defecto (`config.CONFIDENCE_THRESHOLD`) y ajustable por argumento;
  - cuenta cada fotograma una sola vez por marca, aunque tenga varias detecciones de ella;
  - incluye una fila por cada marca de `config.BRANDS`, también las no detectadas (0 s, 0 %).
- Serialización del informe a JSON, por defecto en `outputs/`.
- Tests unitarios de las reglas RD, escritos con TDD.

Fuera de alcance: la detección en vídeo que produce las detecciones (#13), la tabla del informe en el notebook (#14) y la persistencia en base de datos.

## Capabilities

### New Capabilities

- `report`: informe de exposición por marca de un vídeo (tiempo y porcentaje) a partir de las detecciones por fotograma, y su guardado en JSON (RF-05, RD-01…RD-04).

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `src/logo_detector/report.py` y `tests/test_report.py`. Usa `BRANDS`, `CONFIDENCE_THRESHOLD` y `OUTPUTS_DIR`, que ya existen en `config.py`.
- **Dependencias:** ninguna nueva (solo biblioteca estándar).
- **Documentación:** ARCHITECTURE §3, `report` pasa a «Actual» y se describe el informe JSON. README: sin cambios, porque el informe se usará desde el notebook de demo (#14).
- **Contratos:** ninguno todavía. La forma de las detecciones por fotograma que consume `report` queda en el `design.md`; #13 la producirá y, si hace falta, se registrará entonces como contrato.
- **ADR:** ninguno.
