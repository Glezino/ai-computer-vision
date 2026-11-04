## Why

Historia [#14](https://github.com/Glezino/ai-computer-vision/issues/14), la última de la épica E4 (#5) y del Hito 1. Ya existen la detección en imagen (#12), el análisis de vídeo (#13) y el informe de exposición (#11), pero solo se pueden usar escribiendo código. Falta la demo en vivo que pide el briefing: un notebook que las recorra con los pesos entrenados, y un README que explique cómo usarlo. Implementa RF-06 y cierra la presentación de RF-05 (tabla y JSON del informe).

## What Changes

- `notebooks/03_demo.py` (generado como `.ipynb` con `make notebooks`):
  - carga `models/brands.pt`;
  - detecta las marcas en una imagen y la muestra anotada;
  - analiza un vídeo de ejemplo, muestra el vídeo anotado reproducible en el notebook y unos fotogramas con detecciones;
  - calcula el informe de exposición, lo muestra como tabla (marca, detectada, segundos y %) y guarda el JSON en `outputs/`;
  - la imagen, el vídeo y el umbral se cambian en una celda de parámetros al principio.
- `detection`: una vista previa del vídeo anotado en WebM, que el navegador sí reproduce (el `.mp4` con `mp4v` no), sin dependencias nuevas.
- `config.VIDEOS_DIR` (`data/videos/`, no versionado): carpeta de los vídeos de ejemplo de la demo, que aporta la persona.
- README final: demo en local y en Docker, dónde dejar los vídeos, cómo detectar marcas en una imagen propia y estado del proyecto.

Fuera de alcance: front web, base de datos, mejorar el recall del modelo y publicar vídeos de ejemplo en el repositorio.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `notebooks`: añade el notebook de demo `03_demo` (RF-06, RF-05).
- `detection`: añade la vista previa web del vídeo anotado.

## Impact

- **Código:** `notebooks/03_demo.py`, `src/logo_detector/detection.py`, `src/logo_detector/config.py` y `tests/test_detection.py`.
- **Dependencias:** ninguna nueva.
- **Documentación:**
  - README: demo, vídeos de ejemplo, uso de la detección en imagen y estado.
  - ARCHITECTURE: §3, `notebooks` pasa a «Actual»; §5, la vista previa web en el flujo de vídeo; §6, `data/videos/`; §8, prueba de punta a punta de la demo.
  - ADR: ninguno.
- **Contratos:** ninguno.
