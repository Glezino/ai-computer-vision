import json

import pytest

from logo_detector import config
from logo_detector.report import Detection, build_report, save_report


def frames_with(total, *brands_per_frame, confidence=0.9):
    """``total`` fotogramas; los primeros tienen una detección por cada marca indicada."""
    frames = [[Detection(brand, confidence) for brand in brands] for brands in brands_per_frame]
    return frames + [[] for _ in range(total - len(frames))]


def row(report, brand):
    return next(r for r in report.brands if r.brand == brand)


def present(report, brand):
    return row(report, brand).detected


# Una fila por marca


def test_report_has_video_duration_and_one_row_per_brand_in_order():
    report = build_report("demo.mp4", frames_with(100, *[["pepsi"]] * 30), fps=25)

    assert report.video == "demo.mp4"
    assert report.duration_s == 4
    assert [r.brand for r in report.brands] == list(config.BRANDS)
    assert present(report, "pepsi")


def test_undetected_brands_are_reported_with_zero_seconds_and_percentage():
    report = build_report("demo.mp4", frames_with(100, *[["pepsi"]] * 30), fps=25)

    for brand in ("coca-cola", "adidas"):
        assert (row(report, brand).detected, row(report, brand).seconds) == (False, 0)
        assert row(report, brand).percentage == 0


def test_video_without_detections_reports_every_brand_as_undetected():
    report = build_report("empty.mp4", frames_with(10), fps=10)

    assert all(not r.detected and r.seconds == 0 and r.percentage == 0 for r in report.brands)


# Umbral de confianza (RD-01, RD-04)


def test_detection_at_the_default_threshold_counts():
    report = build_report("v.mp4", frames_with(1, ["adidas"], confidence=0.50), fps=1)

    assert report.threshold == config.CONFIDENCE_THRESHOLD
    assert present(report, "adidas")


def test_detection_below_the_default_threshold_does_not_count():
    report = build_report("v.mp4", frames_with(1, ["adidas"], confidence=0.49), fps=1)

    assert not present(report, "adidas")


def test_threshold_can_be_adjusted():
    report = build_report("v.mp4", frames_with(1, ["adidas"], confidence=0.70), 1, threshold=0.8)

    assert report.threshold == 0.8
    assert not present(report, "adidas")


def test_only_detections_above_the_threshold_count_within_a_frame():
    frames = [[Detection("pepsi", 0.3), Detection("pepsi", 0.6)], [Detection("pepsi", 0.3)]]

    report = build_report("v.mp4", frames, fps=1)

    assert row(report, "pepsi").seconds == 1


@pytest.mark.parametrize("threshold", [-0.1, 1.1])
def test_threshold_out_of_range_is_rejected(threshold):
    with pytest.raises(ValueError, match="umbral"):
        build_report("v.mp4", frames_with(1), fps=1, threshold=threshold)


# Tiempo y porcentaje (RD-02, RD-03)


def test_seconds_and_percentage_follow_present_frames_and_fps():
    report = build_report("v.mp4", frames_with(100, *[["coca-cola"]] * 50), fps=25)

    assert row(report, "coca-cola").seconds == 2
    assert row(report, "coca-cola").percentage == 50


def test_several_logos_of_a_brand_in_a_frame_count_once():
    report = build_report("v.mp4", frames_with(4, ["coca-cola"] * 3), fps=2)

    assert row(report, "coca-cola").seconds == 0.5
    assert row(report, "coca-cola").percentage == 25


def test_a_frame_with_several_brands_counts_for_each_of_them():
    report = build_report("v.mp4", frames_with(2, ["coca-cola", "pepsi"]), fps=1)

    assert row(report, "coca-cola").seconds == row(report, "pepsi").seconds == 1


def test_percentage_has_no_rounding_error():
    report = build_report("v.mp4", frames_with(3, ["adidas"]), fps=30)

    assert row(report, "adidas").percentage == 100 / 3


@pytest.mark.parametrize("fps", [0, -25])
def test_non_positive_fps_is_rejected(fps):
    with pytest.raises(ValueError, match="fotogramas por segundo"):
        build_report("v.mp4", frames_with(1), fps=fps)


def test_video_without_frames_is_rejected():
    with pytest.raises(ValueError, match="fotogramas"):
        build_report("v.mp4", [], fps=25)


@pytest.mark.parametrize("confidence", [0.9, 0.1])
def test_unknown_brand_is_rejected_whatever_its_confidence(confidence):
    with pytest.raises(ValueError, match="nike"):
        build_report("v.mp4", frames_with(1, ["nike"], confidence=confidence), fps=1)


# JSON


@pytest.fixture
def report():
    return build_report("demo.mp4", frames_with(100, *[["pepsi"]] * 30), fps=25)


def test_save_report_defaults_to_outputs_dir_and_creates_it(report, tmp_path, monkeypatch):
    outputs = tmp_path / "outputs"
    monkeypatch.setattr(config, "OUTPUTS_DIR", outputs)

    path = save_report(report)

    assert path == outputs / "demo_report.json"
    assert path.is_file()


def test_save_report_writes_to_the_given_path(report, tmp_path):
    path = save_report(report, tmp_path / "custom.json")

    assert path == tmp_path / "custom.json"
    assert path.is_file()


def test_saved_report_round_trips_with_the_same_values(report, tmp_path):
    data = json.loads(save_report(report, tmp_path / "r.json").read_text(encoding="utf-8"))

    assert data == {
        "video": "demo.mp4",
        "duration_s": 4.0,
        "fps": 25,
        "frame_count": 100,
        "threshold": 0.5,
        "brands": [
            {"brand": "coca-cola", "detected": False, "seconds": 0.0, "percentage": 0.0},
            {"brand": "pepsi", "detected": True, "seconds": 1.2, "percentage": 30.0},
            {"brand": "adidas", "detected": False, "seconds": 0.0, "percentage": 0.0},
        ],
    }
