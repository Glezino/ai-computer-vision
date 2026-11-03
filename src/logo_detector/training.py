"""Reentrenamiento del detector con las tres marcas y sus métricas (RF-02, RNF-03, ADR-0001).

Pensado para ejecutarse desde ``notebooks/02_training.py`` en Google Colab con GPU; en CPU
sirve para pruebas cortas (``train(data_yaml, epochs=1, fraction=0.1)``).
"""

import shutil
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import NamedTuple

from ultralytics import YOLO

from logo_detector import config

# Configuración de entrenamiento. Se fija de forma explícita, aunque algunos valores coincidan
# con los de Ultralytics, para que quede documentada y sea reproducible.
TRAIN_CONFIG: dict = {
    # Preprocesamiento: Ultralytics redimensiona con letterbox a imgsz y normaliza a [0, 1].
    "imgsz": config.IMAGE_SIZE,
    # Aumento de datos: flip horizontal (no vertical: un logo invertido no es realista).
    "fliplr": 0.5,
    "flipud": 0.0,
    # Aumento de datos: escala, crop y traslación; mosaic se desactiva en las últimas épocas.
    "scale": 0.5,
    "translate": 0.1,
    "mosaic": 1.0,
    "close_mosaic": 10,
    # Aumento de datos: color jitter en HSV.
    "hsv_h": 0.015,
    "hsv_s": 0.7,
    "hsv_v": 0.4,
    # Entrenamiento.
    "epochs": 100,
    "patience": 20,
    "batch": 16,
    "seed": config.SPLIT_SEED,
    "deterministic": True,
}


class MetricsRow(NamedTuple):
    name: str
    precision: float
    recall: float
    map50: float
    map50_95: float


def train_config(**overrides) -> dict:
    """``TRAIN_CONFIG`` con los parámetros indicados sobrescritos."""
    return {**TRAIN_CONFIG, **overrides}


def train(
    data_yaml: Path = config.DATASET_DIR / "data.yaml",
    base_model: str = config.PRETRAINED_MODEL,
    **overrides,
) -> Path:
    """Reentrena ``base_model`` con el dataset y copia los mejores pesos a ``models/``."""
    config.MODELS_DIR.mkdir(exist_ok=True)
    model = YOLO(config.MODELS_DIR / base_model)
    model.train(
        data=str(data_yaml),
        project=str(config.RUNS_DIR),
        name="brands",
        exist_ok=True,
        **train_config(**overrides),
    )
    weights = config.MODELS_DIR / config.BRAND_MODEL
    shutil.copy2(Path(model.trainer.save_dir) / "weights" / "best.pt", weights)
    return weights


def evaluate(
    weights: Path = config.MODELS_DIR / config.BRAND_MODEL,
    data_yaml: Path = config.DATASET_DIR / "data.yaml",
    split: str = "val",
) -> list[MetricsRow]:
    """Métricas de ``weights`` sobre una partición, global y por marca."""
    model = YOLO(weights)
    metrics = model.val(
        data=str(data_yaml),
        split=split,
        imgsz=config.IMAGE_SIZE,
        project=str(config.RUNS_DIR),
        name=f"brands-{split}",
        exist_ok=True,
    )
    box = metrics.box
    return metrics_rows(
        model.names,
        class_index=box.ap_class_index,
        p=box.p,
        r=box.r,
        ap50=box.ap50,
        ap=box.ap,
        totals=(box.mp, box.mr, box.map50, box.map),
    )


def metrics_rows(
    names: Mapping[int, str],
    class_index: Sequence[int],
    p: Sequence[float],
    r: Sequence[float],
    ap50: Sequence[float],
    ap: Sequence[float],
    totals: tuple[float, float, float, float],
) -> list[MetricsRow]:
    """Fila global y una por marca; las marcas sin ejemplos en la partición salen a cero."""
    per_class = {
        int(c): (float(p[i]), float(r[i]), float(ap50[i]), float(ap[i]))
        for i, c in enumerate(class_index)
    }
    rows = [MetricsRow("todas", *(float(t) for t in totals))]
    rows += [MetricsRow(names[c], *per_class.get(c, (0.0,) * 4)) for c in sorted(names)]
    return rows


def format_metrics(rows: Sequence[MetricsRow]) -> str:
    """Tabla de precisión, recall, mAP@0.5 y mAP@0.5:0.95."""
    header = f"{'marca':<10}{'precisión':>11}{'recall':>9}{'mAP@0.5':>10}{'mAP@0.5:0.95':>14}"
    lines = [header]
    for row in rows:
        lines.append(
            f"{row.name:<10}{row.precision:>11.3f}{row.recall:>9.3f}"
            f"{row.map50:>10.3f}{row.map50_95:>14.3f}"
        )
    return "\n".join(lines)
