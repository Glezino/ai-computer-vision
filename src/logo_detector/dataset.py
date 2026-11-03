"""Preparación del dataset de las tres marcas desde OpenLogo (RF-01, ADR-0003).

Descarga de Hugging Face solo las imágenes con Coca-Cola, Pepsi o Adidas, agrupa las
variantes de cada marca, convierte las cajas a formato YOLO, elimina duplicados y divide
en train, val y test. Uso: ``python -m logo_detector.dataset`` (``make data``).
"""

import hashlib
import json
import logging
import random
import shutil
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from huggingface_hub import hf_hub_download, snapshot_download

from logo_detector import config

logger = logging.getLogger(__name__)

SPLITS = ("train", "val", "test")

# Etiquetas de OpenLogo que corresponden a cada marca, incluidas sus variantes de texto.
OPENLOGO_LABELS = {
    "cocacola": "coca-cola",
    "coke": "coca-cola",
    "pepsi": "pepsi",
    "pepsi_text": "pepsi",
    "pepsi_text1": "pepsi",
    "adidas": "adidas",
    "adidas1": "adidas",
    "adidas_text": "adidas",
}


class Box(NamedTuple):
    """Caja en formato YOLO: índice de la marca en ``config.BRANDS`` y centro y tamaño
    normalizados."""

    brand: int
    cx: float
    cy: float
    w: float
    h: float


@dataclass(frozen=True)
class Sample:
    filepath: str  # ruta relativa dentro del repositorio de OpenLogo
    boxes: tuple[Box, ...]

    @property
    def brands(self) -> set[int]:
        return {box.brand for box in self.boxes}


@dataclass(frozen=True)
class BrandStats:
    images: int
    boxes: int


def to_yolo_box(bbox: Sequence[float]) -> tuple[float, float, float, float]:
    """Convierte ``[x, y, w, h]`` (esquina superior izquierda, FiftyOne) a centro y tamaño,
    recortando la caja a la imagen."""
    x, y, w, h = bbox
    x0, y0 = max(0.0, x), max(0.0, y)
    x1, y1 = min(1.0, x + w), min(1.0, y + h)
    return (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0


def select_samples(raw_samples: Iterable[Mapping]) -> list[Sample]:
    """Muestras de OpenLogo con alguna de las tres marcas, solo con las cajas de esas marcas."""
    selected = []
    for raw in raw_samples:
        boxes = tuple(
            Box(
                config.BRANDS.index(OPENLOGO_LABELS[det["label"]]),
                *to_yolo_box(det["bounding_box"]),
            )
            for det in raw["ground_truth"]["detections"]
            if det["label"] in OPENLOGO_LABELS
        )
        if boxes:
            selected.append(Sample(raw["filepath"], boxes))
    return selected


def drop_duplicates(samples: Iterable[Sample], digest: Callable[[str], str]) -> list[Sample]:
    """Elimina las imágenes con contenido idéntico, conservando la primera por ``filepath``."""
    seen: set[str] = set()
    kept = []
    for sample in sorted(samples, key=lambda s: s.filepath):
        key = digest(sample.filepath)
        if key not in seen:
            seen.add(key)
            kept.append(sample)
    return kept


def split_samples(
    samples: Iterable[Sample], ratios: Sequence[float], seed: int
) -> dict[str, list[Sample]]:
    """Divide en train, val y test estratificando por marca: cada imagen cuenta para la marca
    menos frecuente que contiene. El resultado solo depende de las muestras y la semilla."""
    samples = sorted(samples, key=lambda s: s.filepath)
    frequency = Counter(brand for sample in samples for brand in sample.brands)
    by_brand: dict[int, list[Sample]] = {}
    for sample in samples:
        brand = min(sample.brands, key=lambda b: (frequency[b], b))
        by_brand.setdefault(brand, []).append(sample)

    rng = random.Random(seed)
    splits: dict[str, list[Sample]] = {split: [] for split in SPLITS}
    for brand in sorted(by_brand):
        group = by_brand[brand]
        rng.shuffle(group)
        n_train = round(len(group) * ratios[0])
        n_val = round(len(group) * ratios[1])
        splits["train"] += group[:n_train]
        splits["val"] += group[n_train : n_train + n_val]
        splits["test"] += group[n_train + n_val :]
    return {split: sorted(part, key=lambda s: s.filepath) for split, part in splits.items()}


def compute_stats(splits: Mapping[str, Sequence[Sample]]) -> dict[str, dict[str, BrandStats]]:
    """Imágenes y cajas de cada marca en cada partición."""
    stats = {}
    for split, samples in splits.items():
        images = Counter(brand for sample in samples for brand in sample.brands)
        boxes = Counter(box.brand for sample in samples for box in sample.boxes)
        stats[split] = {
            name: BrandStats(images[i], boxes[i]) for i, name in enumerate(config.BRANDS)
        }
    return stats


def format_stats(splits: Mapping[str, Sequence[Sample]]) -> str:
    """Tabla de imágenes y cajas por marca y partición, con los totales de cada partición."""
    stats = compute_stats(splits)
    header = f"{'marca':<10}" + "".join(f"{split:>18}" for split in splits)
    rows = [header, f"{'':<10}" + f"{'imágenes   cajas':>18}" * len(splits)]
    for brand in config.BRANDS:
        cells = "".join(f"{stats[s][brand].images:>11}{stats[s][brand].boxes:>7}" for s in splits)
        rows.append(f"{brand:<10}{cells}")
    totals = "".join(
        f"{len(samples):>11}{sum(len(x.boxes) for x in samples):>7}" for samples in splits.values()
    )
    rows.append(f"{'total':<10}{totals}")
    return "\n".join(rows)


def download(raw_dir: Path) -> list[Sample]:
    """Descarga las anotaciones y solo las imágenes de las tres marcas en ``raw_dir``."""
    annotations = hf_hub_download(
        config.OPENLOGO_REPO,
        "samples.json",
        repo_type="dataset",
        revision=config.OPENLOGO_REVISION,
        local_dir=raw_dir,
    )
    raw_samples = json.loads(Path(annotations).read_text(encoding="utf-8"))["samples"]
    samples = select_samples(raw_samples)
    logger.info("Descargando %d imágenes con marcas de OpenLogo", len(samples))
    snapshot_download(
        config.OPENLOGO_REPO,
        repo_type="dataset",
        revision=config.OPENLOGO_REVISION,
        local_dir=raw_dir,
        allow_patterns=[sample.filepath for sample in samples],
    )
    return samples


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_dataset(splits: Mapping[str, Sequence[Sample]], raw_dir: Path, out_dir: Path) -> Path:
    """Escribe imágenes, etiquetas YOLO y ``data.yaml``; devuelve la ruta de ``data.yaml``."""
    for folder in ("images", "labels"):
        shutil.rmtree(out_dir / folder, ignore_errors=True)
    for split, samples in splits.items():
        images_dir, labels_dir = out_dir / "images" / split, out_dir / "labels" / split
        images_dir.mkdir(parents=True)
        labels_dir.mkdir(parents=True)
        for sample in samples:
            source = raw_dir / sample.filepath
            shutil.copy2(source, images_dir / source.name)
            lines = (f"{b.brand} {b.cx:.6f} {b.cy:.6f} {b.w:.6f} {b.h:.6f}" for b in sample.boxes)
            (labels_dir / source.with_suffix(".txt").name).write_text("\n".join(lines) + "\n")

    data_yaml = out_dir / "data.yaml"
    names = "\n".join(f"  {i}: {brand}" for i, brand in enumerate(config.BRANDS))
    paths = "\n".join(f"{split}: images/{split}" for split in splits)
    data_yaml.write_text(f"path: {out_dir.resolve().as_posix()}\n{paths}\nnames:\n{names}\n")
    return data_yaml


def prepare(out_dir: Path = config.DATASET_DIR, seed: int = config.SPLIT_SEED) -> Path:
    """Prepara el dataset completo en ``out_dir`` y muestra sus estadísticas."""
    raw_dir = out_dir / "raw"
    samples = download(raw_dir)
    unique = drop_duplicates(samples, lambda filepath: sha256(raw_dir / filepath))
    logger.info("Descartadas %d imágenes duplicadas", len(samples) - len(unique))
    splits = split_samples(unique, config.SPLIT_RATIOS, seed)
    data_yaml = write_dataset(splits, raw_dir, out_dir)
    print(format_stats(splits))
    logger.info("Dataset listo en %s", data_yaml)
    return data_yaml


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)  # una línea por petición HTTP
    prepare()
