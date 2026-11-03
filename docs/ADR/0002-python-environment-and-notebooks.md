# ADR-0002: Entorno Python con uv, Docker y notebooks generados con jupytext

- **Estado:** Aceptado
- **Fecha:** 2026-11-03
- **Decisores:** Victor Gonzalez
- **Relacionado:** RF-06, RNF-01, PROJECT DEC-05

## Contexto

La demo se presenta en notebooks, pero los `.ipynb` dan diffs ilegibles y conflictos en Git. El proyecto debe ser reproducible en Docker.

## Decisión

- Python 3.12 con dependencias gestionadas por uv (`pyproject.toml` y `uv.lock` versionados).
- El código reutilizable vive en el paquete `src/logo_detector/`; los notebooks son scripts `.py` en formato *percent* de jupytext que solo lo orquestan.
- `make notebooks` genera los `.ipynb`, que están en `.gitignore`.
- Una imagen Docker de CPU instala el entorno con uv y arranca Jupyter.

## Alternativas consideradas

- **Versionar los `.ipynb`:** diffs ruidosos y salidas pesadas en el repositorio.
- **pip con `requirements.txt`:** sin lockfile; instalaciones más lentas y menos reproducibles.
- **Python 3.13 o superior:** riesgo de incompatibilidades con PyTorch y sus dependencias.

## Consecuencias

- Diffs limpios y lógica testeable fuera de los notebooks.
- Hay que ejecutar `make notebooks` antes de abrir la demo.
- La imagen Docker es solo de CPU; para entrenar se usa Colab ([ADR-0001](0001-ultralytics-yolo-detector.md)).
