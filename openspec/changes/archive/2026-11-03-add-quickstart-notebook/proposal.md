## Why

Historia [#7](https://github.com/Glezino/ai-computer-vision/issues/7) de la épica E1 (#2), walking skeleton. Ya existen el paquete y el CI (#6), pero falta la capa de notebooks: no hay forma de generar un `.ipynb` ni de comprobar que el detector funciona en el entorno local. Implementa la base de RF-06 según [ADR-0001](../../../docs/ADR/0001-ultralytics-yolo-detector.md) y [ADR-0002](../../../docs/ADR/0002-python-environment-and-notebooks.md) (PROJECT DEC-05).

## What Changes

- Dependencias de Ultralytics y OpenCV en el paquete, con PyTorch de CPU; Jupyter y jupytext en el entorno de desarrollo.
- `notebooks/01_quickstart.py` en formato *percent* de jupytext: carga un YOLO nano preentrenado en COCO y muestra sus detecciones sobre una imagen de ejemplo.
- `make notebooks`: genera un `.ipynb` por cada `notebooks/*.py`; los `.ipynb` siguen sin versionarse.
- README: cómo generar y abrir los notebooks.

Fuera de alcance: el modelo de marcas, el dataset y la anotación propia (E2, E4), el componente `detection` (RF-03, #12) y Docker (#8).

## Capabilities

### New Capabilities

- `notebooks`: generación de los notebooks de demo desde scripts `.py` y notebook de inicio rápido con detecciones de un modelo preentrenado (RF-06).

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `notebooks/01_quickstart.py`; nombre del modelo preentrenado en `src/logo_detector/config.py`.
- **Dependencias:** `pyproject.toml` y `uv.lock` (Ultralytics, OpenCV, PyTorch CPU, Jupyter, jupytext). El job `python` del CI instala más paquetes, pero no cambia sus pasos.
- **Comandos:** `Makefile` (`notebooks`).
- **Documentación:** `README.md` (uso de los notebooks); ARCHITECTURE §2 (Ultralytics, PyTorch, OpenCV y Jupyter pasan a «Actual») y §7 si la implementación diverge.
- **ADR:** aplica ADR-0001 y ADR-0002; no requiere ADR nuevo.
- **Contratos:** ninguno.
