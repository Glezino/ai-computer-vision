"""Informe de exposición por marca a partir de las detecciones por fotograma (RF-05, RD-01…RD-04).

Lógica pura, sin dependencia del modelo: recibe las detecciones que produce ``detection`` y
devuelve, por marca, el tiempo y el porcentaje de la duración del vídeo en que aparece.
"""

import dataclasses
import json
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from logo_detector import config


class Detection(NamedTuple):
    """Detección de una marca en un fotograma, con la confianza en [0, 1]."""

    brand: str
    confidence: float


@dataclass(frozen=True)
class BrandExposure:
    brand: str
    detected: bool
    seconds: float
    percentage: float


@dataclass(frozen=True)
class ExposureReport:
    video: str
    duration_s: float
    fps: float
    frame_count: int
    threshold: float
    brands: tuple[BrandExposure, ...]


def build_report(
    video: str,
    frames: Sequence[Sequence[Detection]],
    fps: float,
    threshold: float = config.CONFIDENCE_THRESHOLD,
    brands: Sequence[str] = config.BRANDS,
) -> ExposureReport:
    """Calcula la exposición de cada marca; ``frames`` tiene una lista por fotograma."""
    if fps <= 0:
        raise ValueError(f"Los fotogramas por segundo deben ser mayores que 0, no {fps}.")
    if not frames:
        raise ValueError(f"El vídeo {video} no tiene fotogramas.")
    if not 0 <= threshold <= 1:
        raise ValueError(f"El umbral de confianza debe estar entre 0 y 1, no {threshold}.")

    # RD-01 y RD-02: una marca está presente si alguna detección llega al umbral, y cada
    # fotograma cuenta una sola vez por marca.
    present = Counter()
    for detections in frames:
        unknown = {d.brand for d in detections} - set(brands)
        if unknown:
            raise ValueError(f"Marcas desconocidas {sorted(unknown)}; se esperaba una de {brands}.")
        present.update({d.brand for d in detections if d.confidence >= threshold})

    frame_count = len(frames)
    rows = tuple(
        BrandExposure(
            brand=brand,
            detected=present[brand] > 0,
            seconds=present[brand] / fps,
            # RD-03, calculado sobre fotogramas para no acumular error de redondeo.
            percentage=100 * present[brand] / frame_count,
        )
        for brand in brands
    )
    return ExposureReport(video, frame_count / fps, fps, frame_count, threshold, rows)


def save_report(report: ExposureReport, path: Path | None = None) -> Path:
    """Guarda el informe en JSON; por defecto en ``outputs/<vídeo>_report.json``."""
    if path is None:
        path = config.OUTPUTS_DIR / f"{Path(report.video).stem}_report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(dataclasses.asdict(report), indent=2, ensure_ascii=False)
    path.write_text(data + "\n", encoding="utf-8")
    return path
