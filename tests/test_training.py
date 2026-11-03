from logo_detector import config
from logo_detector.training import (
    TRAIN_CONFIG,
    MetricsRow,
    format_metrics,
    metrics_rows,
    train_config,
)

NAMES = {0: "coca-cola", 1: "pepsi", 2: "adidas"}


# Métricas


def test_metrics_rows_has_a_global_row_and_one_per_brand():
    rows = metrics_rows(
        NAMES,
        class_index=[0, 1, 2],
        p=[0.9, 0.8, 0.7],
        r=[0.6, 0.5, 0.4],
        ap50=[0.85, 0.75, 0.65],
        ap=[0.55, 0.45, 0.35],
        totals=(0.8, 0.5, 0.75, 0.45),
    )
    assert rows == [
        MetricsRow("todas", 0.8, 0.5, 0.75, 0.45),
        MetricsRow("coca-cola", 0.9, 0.6, 0.85, 0.55),
        MetricsRow("pepsi", 0.8, 0.5, 0.75, 0.45),
        MetricsRow("adidas", 0.7, 0.4, 0.65, 0.35),
    ]


def test_metrics_rows_reports_absent_brands_as_zero():
    rows = metrics_rows(
        NAMES, class_index=[1], p=[0.8], r=[0.5], ap50=[0.7], ap=[0.4], totals=(0.8, 0.5, 0.7, 0.4)
    )
    assert rows[1] == MetricsRow("coca-cola", 0.0, 0.0, 0.0, 0.0)
    assert rows[2] == MetricsRow("pepsi", 0.8, 0.5, 0.7, 0.4)


def test_format_metrics_shows_every_row_and_metric():
    table = format_metrics(
        [MetricsRow("todas", 0.8, 0.5, 0.75, 0.456), MetricsRow("pepsi", 1, 0, 0, 0)]
    )
    lines = table.splitlines()
    assert ["precisión", "recall", "mAP@0.5", "mAP@0.5:0.95"] == lines[0].split()[1:]
    assert lines[1].split() == ["todas", "0.800", "0.500", "0.750", "0.456"]
    assert lines[2].split()[0] == "pepsi"


# Configuración


def test_train_config_documents_preprocessing_and_augmentation():
    assert TRAIN_CONFIG["imgsz"] == config.IMAGE_SIZE
    for key in ("fliplr", "scale", "translate", "hsv_h", "hsv_s", "hsv_v", "mosaic", "seed"):
        assert key in TRAIN_CONFIG


def test_train_config_override_changes_only_that_parameter():
    custom = train_config(epochs=1)
    assert custom["epochs"] == 1
    assert {k: v for k, v in custom.items() if k != "epochs"} == {
        k: v for k, v in TRAIN_CONFIG.items() if k != "epochs"
    }
    assert TRAIN_CONFIG["epochs"] != 1
