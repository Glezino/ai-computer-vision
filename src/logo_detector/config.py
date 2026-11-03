"""Parámetros por defecto del proyecto (ARCHITECTURE §6).

Los componentes los usan como valor por defecto y permiten sobrescribirlos por argumento.
"""

from pathlib import Path

# Marcas de la prueba de concepto (PROJECT DEC-01).
BRANDS: tuple[str, ...] = ("coca-cola", "pepsi", "adidas")

# Rutas de trabajo, relativas a la raíz del repositorio; ninguna se versiona.
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
OUTPUTS_DIR = ROOT_DIR / "outputs"
RUNS_DIR = ROOT_DIR / "runs"

# Umbral de confianza por defecto de las detecciones (RD-04).
CONFIDENCE_THRESHOLD = 0.5

# Detector YOLO nano preentrenado en COCO; Ultralytics lo descarga en MODELS_DIR (ADR-0001).
PRETRAINED_MODEL = "yolo26n.pt"

# Pesos del modelo de marcas reentrenado, en MODELS_DIR (RF-02).
BRAND_MODEL = "brands.pt"

# Tamaño de imagen de entrada del detector, en píxeles (valor por defecto de YOLO).
IMAGE_SIZE = 640

# Dataset de partida OpenLogo en Hugging Face, fijado a una revisión (PROJECT DEC-02, ADR-0003).
OPENLOGO_REPO = "Voxel51/OpenLogo"
OPENLOGO_REVISION = "65b6e930d04cda8a229d2a3bf1aacb5ea6a85838"
DATASET_DIR = DATA_DIR / "openlogo"

# Particiones train/val/test y semilla de la división (RF-01).
SPLIT_RATIOS = (0.7, 0.15, 0.15)
SPLIT_SEED = 42
