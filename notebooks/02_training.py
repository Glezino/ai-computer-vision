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
# # Entrenamiento del modelo de marcas
#
# Reentrena YOLO26 nano, preentrenado en COCO, con el dataset de Coca-Cola, Pepsi y Adidas,
# y muestra las métricas de validación global y por marca (RF-02, RNF-03).
#
# **En Google Colab:** *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU* y
# ejecuta todo. El notebook clona el repositorio, instala el paquete, prepara el dataset,
# entrena (una hora aproximadamente con una GPU T4) y descarga `brands.pt`. Cópialo a
# `models/` del proyecto.
#
# **En local** funciona igual, pero en CPU solo es práctico con un entrenamiento corto
# (ver `OVERRIDES`).

# %%
import subprocess
import sys
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
REPO = "https://github.com/Glezino/ai-computer-vision.git"
BRANCH = "dev"  # rama del repositorio que se entrena en Colab
OVERRIDES: dict = {}  # p. ej. {"epochs": 1, "fraction": 0.1} para una prueba corta en CPU

if IN_COLAB:
    print(sys.version)
    project = Path("/content/ai-computer-vision")
    if not project.exists():
        subprocess.run(["git", "clone", "--branch", BRANCH, REPO, str(project)], check=True)
    # Colab no usa Python 3.12 (ADR-0002); el paquete no depende de nada específico de esa
    # versión, así que se instala igualmente sobre el PyTorch con CUDA que trae Colab.
    pip = [sys.executable, "-m", "pip", "install", "-q", "--ignore-requires-python"]
    subprocess.run([*pip, "-e", str(project)], check=True)
    sys.path.insert(0, str(project / "src"))
    subprocess.run(["nvidia-smi", "-L"], check=False)

# %%
from logo_detector import dataset  # noqa: E402
from logo_detector.training import TRAIN_CONFIG, evaluate, format_metrics, train  # noqa: E402

# %% [markdown]
# ## Configuración de preprocesamiento y aumento de datos

# %%
for key, value in {**TRAIN_CONFIG, **OVERRIDES}.items():
    print(f"{key:<14}{value}")

# %% [markdown]
# ## Dataset

# %%
data_yaml = dataset.prepare()

# %% [markdown]
# ## Entrenamiento

# %%
weights = train(data_yaml, **OVERRIDES)
print(f"Pesos guardados en {weights}")

# %% [markdown]
# ## Métricas de validación

# %%
print(format_metrics(evaluate(weights, data_yaml)))

# %% [markdown]
# ## Descargar los pesos (Colab)

# %%
if IN_COLAB:
    from google.colab import files

    files.download(str(weights))
