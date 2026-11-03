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

# Umbral de confianza por defecto de las detecciones (RD-04).
CONFIDENCE_THRESHOLD = 0.5

# Detector YOLO nano preentrenado en COCO; Ultralytics lo descarga en MODELS_DIR (ADR-0001).
PRETRAINED_MODEL = "yolo26n.pt"

# Tamaño de imagen de entrada del detector, en píxeles (valor por defecto de YOLO).
IMAGE_SIZE = 640
