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
# # Inicio rápido: detección con YOLO preentrenado
#
# Comprueba que el entorno funciona: carga un detector YOLO nano preentrenado en COCO y
# muestra sus detecciones sobre una imagen de ejemplo que incluye Ultralytics. No necesita
# datos ni pesos propios del proyecto. La primera ejecución descarga los pesos en `models/`.

# %%
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils import ASSETS

from logo_detector import config

# %% [markdown]
# ## Cargar el modelo

# %%
config.MODELS_DIR.mkdir(exist_ok=True)
model = YOLO(config.MODELS_DIR / config.PRETRAINED_MODEL)

# %% [markdown]
# ## Detectar sobre la imagen de ejemplo

# %%
image_path = ASSETS / "bus.jpg"
result = model.predict(image_path, conf=config.CONFIDENCE_THRESHOLD, imgsz=config.IMAGE_SIZE)[0]

for box in result.boxes:
    print(f"{result.names[int(box.cls)]:<12} {float(box.conf):.2f}")

# %% [markdown]
# ## Imagen con las detecciones

# %%
annotated = result.plot()  # BGR, con caja, clase y confianza
Image.fromarray(annotated[..., ::-1])
