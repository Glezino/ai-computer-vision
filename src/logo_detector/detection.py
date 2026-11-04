"""Detección de las marcas en una imagen y anotación con caja, marca y confianza (RF-03, RD-04).

La inferencia la hace Ultralytics; el filtrado por umbral y el dibujo son funciones puras para
poder probarlos sin modelo.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

import cv2
import numpy as np
from ultralytics import YOLO

from logo_detector import config

# Un color BGR fijo por marca, en el orden de config.BRANDS, y otro para marcas desconocidas.
BRAND_COLORS: tuple[tuple[int, int, int], ...] = ((40, 40, 220), (200, 110, 20), (30, 30, 30))
DEFAULT_COLOR = (0, 200, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX


class BrandBox(NamedTuple):
    """Detección de una marca con la confianza en [0, 1] y la caja (x1, y1, x2, y2) en píxeles."""

    brand: str
    confidence: float
    box: tuple[int, int, int, int]


class ImageDetection(NamedTuple):
    """Imagen anotada (BGR) y las detecciones que se han dibujado en ella."""

    image: np.ndarray
    detections: list[BrandBox]


def load_model(weights: Path = config.MODELS_DIR / config.BRAND_MODEL) -> YOLO:
    """Carga el detector de marcas; falla con instrucciones si no están los pesos."""
    weights = Path(weights)
    if not weights.is_file():
        raise FileNotFoundError(
            f"No se encuentran los pesos del modelo en {weights}. Entrénalo con el notebook "
            "02_training y copia brands.pt a models/ (README, «Modelo de marcas»)."
        )
    return YOLO(weights)


def detect_image(
    model: YOLO,
    image: str | Path | np.ndarray,
    threshold: float = config.CONFIDENCE_THRESHOLD,
) -> ImageDetection:
    """Detecta las marcas en una imagen (ruta o matriz BGR) y la devuelve anotada."""
    _check_threshold(threshold)
    pixels = _read_image(image) if isinstance(image, str | Path) else image
    result = model.predict(pixels, conf=threshold, imgsz=config.IMAGE_SIZE, verbose=False)[0]
    detections = select_detections(result, threshold)
    return ImageDetection(draw_detections(pixels, detections), detections)


def select_detections(result, threshold: float = config.CONFIDENCE_THRESHOLD) -> list[BrandBox]:
    """Convierte un resultado de Ultralytics en las detecciones con confianza >= ``threshold``."""
    _check_threshold(threshold)
    boxes = result.boxes
    return [
        BrandBox(result.names[int(cls)], float(conf), tuple(round(v) for v in xyxy))
        for cls, conf, xyxy in zip(
            boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist(), strict=True
        )
        if conf >= threshold
    ]


def label(detection: BrandBox) -> str:
    """Texto bajo la caja: marca y confianza en porcentaje entero (``pepsi 87 %``)."""
    return f"{detection.brand} {round(detection.confidence * 100)} %"


def draw_detections(image: np.ndarray, detections: Sequence[BrandBox]) -> np.ndarray:
    """Devuelve una copia de ``image`` con cada caja y su etiqueta debajo, dentro de la imagen."""
    annotated = image.copy()
    height, width = annotated.shape[:2]
    thickness = max(1, round(min(height, width) / 300))
    font_scale = max(0.4, min(height, width) / 1000)
    padding = 2 * thickness

    for detection in detections:
        x1, y1, x2, y2 = detection.box
        color = _brand_color(detection.brand)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)

        text = label(detection)
        (text_w, text_h), baseline = cv2.getTextSize(text, FONT, font_scale, thickness)
        label_w, label_h = text_w + 2 * padding, text_h + baseline + 2 * padding
        # Debajo de la caja; si no cabe, se sube y se desplaza para no salirse de la imagen.
        top = min(y2 + thickness, height - label_h)
        left = max(0, min(x1, width - label_w))
        cv2.rectangle(annotated, (left, top), (left + label_w, top + label_h), color, cv2.FILLED)
        cv2.putText(
            annotated,
            text,
            (left + padding, top + padding + text_h),
            FONT,
            font_scale,
            _text_color(color),
            thickness,
            cv2.LINE_AA,
        )
    return annotated


def _check_threshold(threshold: float) -> None:
    if not 0 <= threshold <= 1:
        raise ValueError(f"El umbral de confianza debe estar entre 0 y 1, no {threshold}.")


def _read_image(path: str | Path) -> np.ndarray:
    pixels = cv2.imread(str(path))
    if pixels is None:
        raise ValueError(f"No se puede leer la imagen {path}: no existe o no es una imagen.")
    return pixels


def _brand_color(brand: str) -> tuple[int, int, int]:
    if brand in config.BRANDS:
        return BRAND_COLORS[config.BRANDS.index(brand)]
    return DEFAULT_COLOR


def _text_color(background: tuple[int, int, int]) -> tuple[int, int, int]:
    blue, green, red = background
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    return (0, 0, 0) if luminance > 140 else (255, 255, 255)
