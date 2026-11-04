"""Detección de las marcas en imágenes y vídeos, anotadas con caja, marca y confianza.

Implementa RF-03, RF-04 y RD-04. La inferencia la hace Ultralytics; el filtrado por umbral y el
dibujo son funciones puras para poder probarlos sin modelo.
"""

import logging
import math
import time
from collections.abc import Callable, Sequence
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
# MPEG-4 Part 2: el único códec de .mp4 que incluye opencv-python (no trae H.264).
VIDEO_CODEC = cv2.VideoWriter_fourcc(*"mp4v")
# VP8 en WebM: lo reproducen los navegadores y opencv-python lo incluye (vista previa).
WEB_CODEC = cv2.VideoWriter_fourcc(*"VP80")

logger = logging.getLogger(__name__)


class BrandBox(NamedTuple):
    """Detección de una marca con la confianza en [0, 1] y la caja (x1, y1, x2, y2) en píxeles."""

    brand: str
    confidence: float
    box: tuple[int, int, int, int]


class ImageDetection(NamedTuple):
    """Imagen anotada (BGR) y las detecciones que se han dibujado en ella."""

    image: np.ndarray
    detections: list[BrandBox]


class VideoAnalysis(NamedTuple):
    """Vídeo anotado, sus fps, las detecciones de cada fotograma y el tiempo de procesado."""

    output: Path
    fps: float
    frames: list[list[BrandBox]]
    elapsed_s: float


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


def analyze_video(
    model: YOLO,
    video: str | Path,
    output: str | Path | None = None,
    threshold: float = config.CONFIDENCE_THRESHOLD,
) -> VideoAnalysis:
    """Detecta las marcas en cada fotograma y escribe el vídeo anotado (RF-04).

    Por defecto lo guarda en ``outputs/<vídeo>_annotated.mp4``. Las detecciones por fotograma
    y los fps sirven tal cual para ``report.build_report``.
    """
    _check_threshold(threshold)
    video = Path(video)
    output = Path(output) if output else config.OUTPUTS_DIR / f"{video.stem}_annotated.mp4"
    frames: list[list[BrandBox]] = []

    def annotate(frame: np.ndarray) -> np.ndarray:
        annotated, detections = detect_image(model, frame, threshold)
        frames.append(detections)
        return annotated

    start = time.perf_counter()
    fps = _transform_video(video, output, VIDEO_CODEC, annotate)
    elapsed = time.perf_counter() - start
    logger.info(
        "%s: %d fotogramas en %.1f s (%.1f fotogramas/s)",
        video.name,
        len(frames),
        elapsed,
        len(frames) / elapsed if elapsed else 0,
    )
    return VideoAnalysis(output, fps, frames, elapsed)


def web_preview(video: str | Path, output: str | Path | None = None, max_width: int = 960) -> Path:
    """Copia el vídeo en WebM (VP8), que el navegador reproduce, reducido a ``max_width``.

    Por defecto se guarda junto al vídeo con extensión ``.webm``. Conserva fotogramas y fps.
    """
    video = Path(video)
    output = Path(output) if output else video.with_suffix(".webm")

    def shrink(frame: np.ndarray) -> np.ndarray:
        height, width = frame.shape[:2]
        if width <= max_width:
            return frame
        new_height = round(height * max_width / width / 2) * 2  # par, como piden los códecs
        return cv2.resize(frame, (max_width, new_height), interpolation=cv2.INTER_AREA)

    _transform_video(video, output, WEB_CODEC, shrink)
    return output


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


def _transform_video(
    video: Path, output: Path, codec: int, transform: Callable[[np.ndarray], np.ndarray]
) -> float:
    """Escribe en ``output`` cada fotograma de ``video`` tras ``transform``; devuelve los fps.

    Falla con la ruta si el vídeo no existe o no es legible, y no deja un vídeo parcial.
    """
    capture = cv2.VideoCapture(str(video)) if video.is_file() else None
    writer = None
    try:
        if capture is None or not capture.isOpened():
            raise ValueError(f"No se puede abrir el vídeo {video}: no existe o no es un vídeo.")
        fps = capture.get(cv2.CAP_PROP_FPS)
        ok, frame = capture.read()
        if not ok or not math.isfinite(fps) or fps <= 0:
            raise ValueError(f"El vídeo {video} no tiene fotogramas legibles o fps válidos.")

        output.parent.mkdir(parents=True, exist_ok=True)
        while ok:
            result = transform(frame)
            if writer is None:
                height, width = result.shape[:2]
                writer = cv2.VideoWriter(str(output), codec, fps, (width, height))
            writer.write(result)
            ok, frame = capture.read()
    except BaseException:
        if writer is not None:
            writer.release()
            writer = None
            output.unlink(missing_ok=True)  # no dejar un vídeo parcial que parezca válido
        raise
    finally:
        if writer is not None:
            writer.release()
        if capture is not None:
            capture.release()
    return fps


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
