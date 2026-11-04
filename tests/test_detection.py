from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from logo_detector import config
from logo_detector.detection import (
    BrandBox,
    detect_image,
    draw_detections,
    label,
    load_model,
    select_detections,
)

NAMES = {0: "coca-cola", 1: "pepsi", 2: "adidas"}


def fake_result(*boxes):
    """Resultado de Ultralytics con ``boxes`` como (clase, confianza, x1, y1, x2, y2)."""
    rows = np.array(boxes, dtype=float).reshape(-1, 6)
    return SimpleNamespace(
        names=NAMES,
        boxes=SimpleNamespace(cls=rows[:, 0], conf=rows[:, 1], xyxy=rows[:, 2:]),
    )


# Umbral


def test_select_keeps_only_detections_at_or_above_default_threshold():
    result = fake_result((1, 0.70, 10, 20, 110, 80.6), (2, 0.30, 0, 0, 5, 5))

    assert select_detections(result) == [BrandBox("pepsi", 0.70, (10, 20, 110, 81))]


def test_select_keeps_confidence_equal_to_threshold():
    result = fake_result((2, 0.50, 0, 0, 5, 5))

    assert [d.brand for d in select_detections(result)] == ["adidas"]


def test_select_with_adjusted_threshold():
    result = fake_result((2, 0.70, 0, 0, 5, 5))

    assert select_detections(result, threshold=0.8) == []


def test_select_without_boxes_returns_empty_list():
    assert select_detections(fake_result()) == []


@pytest.mark.parametrize("threshold", [-0.1, 1.5])
def test_select_rejects_threshold_outside_0_1(threshold):
    with pytest.raises(ValueError, match="entre 0 y 1"):
        select_detections(fake_result(), threshold=threshold)


# Dibujo


def black_image(height=200, width=200):
    return np.zeros((height, width, 3), dtype=np.uint8)


def test_label_shows_brand_and_rounded_percentage():
    assert label(BrandBox("pepsi", 0.874, (0, 0, 1, 1))) == "pepsi 87 %"


def test_draw_without_detections_returns_identical_copy():
    image = black_image()

    annotated = draw_detections(image, [])

    assert annotated is not image
    assert np.array_equal(annotated, image)


def test_draw_frames_the_box_and_writes_the_label_below():
    image = black_image()

    annotated = draw_detections(image, [BrandBox("pepsi", 0.87, (40, 40, 160, 100))])

    assert annotated[40, 100].any()  # borde superior de la caja
    assert not annotated[70, 100].any()  # interior de la caja, sin rellenar
    assert annotated[105:130, 40:160].any()  # etiqueta debajo de la caja
    assert not annotated[10:35].any()  # nada encima de la caja


def test_draw_keeps_the_label_inside_the_image_at_the_bottom_edge():
    image = black_image()

    annotated = draw_detections(image, [BrandBox("adidas", 0.9, (40, 100, 160, 199))])

    # La etiqueta no cabe debajo: se sube y su fondo queda dentro de la caja, junto al borde.
    assert annotated[195, 60].any()


def test_draw_does_not_modify_the_original():
    image = black_image()

    draw_detections(image, [BrandBox("pepsi", 0.87, (40, 40, 160, 100))])

    assert not image.any()


# Detección en imagen sin modelo


class FakeModel:
    """Modelo que devuelve siempre el mismo resultado y guarda los argumentos de ``predict``."""

    def __init__(self, result):
        self.result = result
        self.calls = []

    def predict(self, image, **kwargs):
        self.calls.append((image, kwargs))
        return [self.result]


def test_detect_image_returns_annotated_copy_and_detections():
    image = black_image()
    model = FakeModel(fake_result((1, 0.87, 40, 40, 160, 100), (0, 0.2, 0, 0, 5, 5)))

    annotated, detections = detect_image(model, image)

    assert detections == [BrandBox("pepsi", 0.87, (40, 40, 160, 100))]
    assert annotated.any()
    assert not image.any()
    assert model.calls[0][1]["conf"] == config.CONFIDENCE_THRESHOLD


def test_detect_image_without_logos_returns_the_image_unchanged():
    image = black_image()

    annotated, detections = detect_image(FakeModel(fake_result()), image)

    assert detections == []
    assert np.array_equal(annotated, image)


def test_detect_image_reads_an_image_path(tmp_path):
    path = tmp_path / "sample.png"
    assert cv2.imwrite(str(path), black_image())
    model = FakeModel(fake_result())

    detect_image(model, path)

    assert model.calls[0][0].shape == (200, 200, 3)


def test_detect_image_rejects_invalid_threshold():
    with pytest.raises(ValueError, match="entre 0 y 1"):
        detect_image(FakeModel(fake_result()), black_image(), threshold=1.5)


def test_detect_image_with_missing_path_names_it(tmp_path):
    path = tmp_path / "missing.jpg"

    with pytest.raises(ValueError, match="missing.jpg"):
        detect_image(FakeModel(fake_result()), path)


def test_detect_image_with_a_file_that_is_not_an_image_names_it(tmp_path):
    path = tmp_path / "notes.jpg"
    path.write_text("no soy una imagen")

    with pytest.raises(ValueError, match="notes.jpg"):
        detect_image(FakeModel(fake_result()), path)


def test_load_model_without_weights_explains_how_to_get_them(tmp_path):
    weights = tmp_path / "brands.pt"

    with pytest.raises(FileNotFoundError, match="02_training") as error:
        load_model(weights)

    assert str(weights) in str(error.value)


# Integración con el modelo entrenado (no corre en el CI: los pesos y el dataset no se versionan)

SAMPLE_IMAGE = config.DATASET_DIR / "images" / "test" / "60524367.jpg"  # logos de Pepsi
BRAND_WEIGHTS = config.MODELS_DIR / config.BRAND_MODEL


@pytest.mark.skipif(not BRAND_WEIGHTS.is_file(), reason="faltan los pesos models/brands.pt")
@pytest.mark.skipif(not SAMPLE_IMAGE.is_file(), reason="falta el dataset (make data)")
def test_brand_model_detects_pepsi_in_a_sample_image():
    original = cv2.imread(str(SAMPLE_IMAGE))

    annotated, detections = detect_image(load_model(), SAMPLE_IMAGE)

    assert "pepsi" in {d.brand for d in detections}
    assert all(d.confidence >= config.CONFIDENCE_THRESHOLD for d in detections)
    assert annotated.shape == original.shape
    assert not np.array_equal(annotated, original)
