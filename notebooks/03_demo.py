# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Demo: detección de marcas e informe de exposición
#
# Recorre el producto con el modelo de marcas entrenado (Coca-Cola, Pepsi y Adidas):
#
# 1. detecta las marcas en una imagen;
# 2. analiza un vídeo y genera el vídeo anotado;
# 3. calcula cuánto tiempo y qué porcentaje del vídeo aparece cada marca, y lo guarda en JSON.
#
# Necesita los pesos `models/brands.pt` y un vídeo en `data/videos/` (ver README, «Demo»).
# Para usar otra imagen, otro vídeo u otro umbral, cambia la celda de parámetros y ejecuta todo.

# %%
import os
from pathlib import Path

import cv2
import numpy as np
from IPython.display import Markdown, Video, display
from PIL import Image

from logo_detector import config, detection, report


def show(bgr: np.ndarray) -> Image.Image:
    """Imagen de OpenCV (BGR) lista para mostrarse en el notebook."""
    return Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))


# %% [markdown]
# ## Parámetros

# %%
IMAGE = config.DATASET_DIR / "images" / "test" / "60524367.jpg"
VIDEO = config.VIDEOS_DIR / "demo.mp4"
THRESHOLD = config.CONFIDENCE_THRESHOLD  # 0.5: confianza mínima de una detección


# %% [markdown]
# ## Modelo

# %%
model = detection.load_model()
print("Marcas:", ", ".join(model.names.values()))

# %% [markdown]
# ## 1. Detección en una imagen
#
# Cada logo por encima del umbral aparece enmarcado, con la marca y la confianza debajo.

# %%
annotated, found = detection.detect_image(model, IMAGE, THRESHOLD)
for d in found:
    print(detection.label(d))
show(annotated)

# %% [markdown]
# ## 2. Análisis del vídeo
#
# Se procesan todos los fotogramas en CPU (alrededor de 1 minuto por minuto de vídeo). El vídeo
# anotado se guarda en `outputs/` como `.mp4` (resolución original) y, para verlo aquí, como
# vista previa `.webm`.

# %%
analysis = detection.analyze_video(model, VIDEO, threshold=THRESHOLD)
with_logo = sum(bool(frame) for frame in analysis.frames)
print(f"Vídeo anotado: {analysis.output}")
print(f"{len(analysis.frames)} fotogramas a {analysis.fps:.0f} fps")
print(f"Procesado en {analysis.elapsed_s:.0f} s")
print(f"Fotogramas con alguna marca: {with_logo}")

# %%
preview = detection.web_preview(analysis.output)
Video(Path(os.path.relpath(preview)).as_posix(), html_attributes="controls loop", width=640)

# %% [markdown]
# Algunos fotogramas con detecciones, repartidos a lo largo del vídeo:

# %%
hits = [i for i, frame in enumerate(analysis.frames) if frame]
picked = [hits[round(k * (len(hits) - 1) / 5)] for k in range(6)] if hits else []
capture = cv2.VideoCapture(str(analysis.output))
tiles = []
for index in dict.fromkeys(picked):
    capture.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, frame = capture.read()
    if ok:
        height = 240
        tile = cv2.resize(frame, (round(frame.shape[1] * height / frame.shape[0]), height))
        cv2.putText(
            tile,
            f"{index / analysis.fps:.1f} s",
            (8, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
        tiles.append(tile)
capture.release()
show(np.hstack(tiles)) if tiles else print("No hay fotogramas con detecciones.")

# %% [markdown]
# ## 3. Informe de exposición
#
# Una marca está presente en un fotograma si alguna de sus detecciones llega al umbral; su
# tiempo es el número de esos fotogramas entre los fps, y el porcentaje, ese tiempo sobre la
# duración del vídeo.

# %%
exposure = report.build_report(Path(VIDEO).name, analysis.frames, analysis.fps, THRESHOLD)
rows = "\n".join(
    f"| {b.brand} | {'sí' if b.detected else 'no'} | {b.seconds:.1f} | {b.percentage:.1f} % |"
    for b in exposure.brands
)
display(
    Markdown(
        f"**{exposure.video}**: {exposure.duration_s:.1f} s, umbral {exposure.threshold:.0%}\n\n"
        "| Marca | Detectada | Segundos | % del vídeo |\n|---|---|---|---|\n" + rows
    )
)

# %%
print("Informe guardado en", report.save_report(exposure))
