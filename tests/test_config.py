from logo_detector import config


def test_default_brands_are_the_three_poc_brands():
    assert config.BRANDS == ("coca-cola", "pepsi", "adidas")


def test_default_confidence_threshold_is_a_probability():
    assert 0 < config.CONFIDENCE_THRESHOLD < 1


def test_work_dirs_live_in_the_repository_root():
    for path in (config.DATA_DIR, config.MODELS_DIR, config.OUTPUTS_DIR):
        assert path.parent == config.ROOT_DIR
