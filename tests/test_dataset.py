import pytest

from logo_detector import config
from logo_detector.dataset import (
    Box,
    Sample,
    compute_stats,
    drop_duplicates,
    select_samples,
    split_samples,
    to_yolo_box,
)

COCA_COLA, PEPSI, ADIDAS = range(3)


def raw_sample(filepath, *labels):
    """Muestra de OpenLogo en formato FiftyOne con una caja por etiqueta."""
    detections = [{"label": label, "bounding_box": [0.1, 0.2, 0.4, 0.2]} for label in labels]
    return {"filepath": filepath, "ground_truth": {"detections": detections}}


def sample(filepath, *brands):
    return Sample(filepath, tuple(Box(brand, 0.5, 0.5, 0.1, 0.1) for brand in brands))


# Conversión de cajas


def test_to_yolo_box_converts_top_left_to_center():
    assert to_yolo_box([0.1, 0.2, 0.4, 0.2]) == pytest.approx((0.3, 0.3, 0.4, 0.2))


def test_to_yolo_box_clips_to_the_image():
    cx, cy, w, h = to_yolo_box([-0.1, 0.9, 0.3, 0.2])
    assert (cx - w / 2, cx + w / 2) == pytest.approx((0.0, 0.2))
    assert (cy - h / 2, cy + h / 2) == pytest.approx((0.9, 1.0))


# Selección de muestras


def test_select_samples_groups_brand_variants():
    raw = [raw_sample("data/a.jpg", "adidas", "adidas1", "adidas_text", "coke", "pepsi_text1")]
    [selected] = select_samples(raw)
    assert [box.brand for box in selected.boxes] == [ADIDAS, ADIDAS, ADIDAS, COCA_COLA, PEPSI]


def test_select_samples_drops_other_logos_and_images_without_brands():
    raw = [raw_sample("data/a.jpg", "cocacola", "nike"), raw_sample("data/b.jpg", "nike")]
    [selected] = select_samples(raw)
    assert selected.filepath == "data/a.jpg"
    assert [box.brand for box in selected.boxes] == [COCA_COLA]


def test_select_samples_converts_boxes_to_yolo():
    [selected] = select_samples([raw_sample("data/a.jpg", "pepsi")])
    assert selected.boxes[0] == pytest.approx(Box(PEPSI, 0.3, 0.3, 0.4, 0.2))


# Duplicados


def test_drop_duplicates_keeps_the_first_file_with_the_same_content():
    samples = [
        sample("data/b.jpg", PEPSI),
        sample("data/a.jpg", PEPSI),
        sample("data/c.jpg", ADIDAS),
    ]
    digests = {"data/a.jpg": "x", "data/b.jpg": "x", "data/c.jpg": "y"}
    kept = drop_duplicates(samples, digests.__getitem__)
    assert [s.filepath for s in kept] == ["data/a.jpg", "data/c.jpg"]


# División


def brand_samples():
    samples = [sample(f"data/coca{i}.jpg", COCA_COLA) for i in range(100)]
    samples += [sample(f"data/pepsi{i}.jpg", PEPSI) for i in range(60)]
    samples += [sample(f"data/adidas{i}.jpg", ADIDAS) for i in range(40)]
    samples += [sample(f"data/mix{i}.jpg", COCA_COLA, ADIDAS) for i in range(20)]
    return samples


def test_split_samples_puts_each_image_in_exactly_one_split():
    samples = brand_samples()
    splits = split_samples(samples, config.SPLIT_RATIOS, seed=1)
    paths = [s.filepath for part in splits.values() for s in part]
    assert sorted(paths) == sorted(s.filepath for s in samples)


def test_split_samples_is_deterministic_for_a_seed():
    samples = brand_samples()
    first = split_samples(samples, config.SPLIT_RATIOS, seed=1)
    second = split_samples(list(reversed(samples)), config.SPLIT_RATIOS, seed=1)
    assert first == second


def test_split_samples_keeps_the_ratios_for_each_brand():
    splits = split_samples(brand_samples(), config.SPLIT_RATIOS, seed=1)
    stats = compute_stats(splits)
    for brand in config.BRANDS:
        images = [stats[split][brand].images for split in ("train", "val", "test")]
        total = sum(images)
        for count, ratio in zip(images, config.SPLIT_RATIOS, strict=True):
            assert count / total == pytest.approx(ratio, abs=0.05)


# Estadísticas


def test_compute_stats_counts_images_and_boxes_per_brand_and_split():
    splits = {
        "train": [sample("data/a.jpg", PEPSI, PEPSI), sample("data/b.jpg", PEPSI, ADIDAS)],
        "val": [sample("data/c.jpg", COCA_COLA)],
        "test": [],
    }
    stats = compute_stats(splits)
    assert (stats["train"]["pepsi"].images, stats["train"]["pepsi"].boxes) == (2, 3)
    assert (stats["train"]["adidas"].images, stats["train"]["adidas"].boxes) == (1, 1)
    assert (stats["val"]["coca-cola"].images, stats["val"]["coca-cola"].boxes) == (1, 1)
    assert (stats["test"]["coca-cola"].images, stats["test"]["coca-cola"].boxes) == (0, 0)
