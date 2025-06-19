from breathe_config import BreatheConfig


def test_breathe_config_getters_offset_values():
    breathe_config = BreatheConfig()
    assert breathe_config._breathe_in > breathe_config.breathe_in
    assert breathe_config._breathe_out > breathe_config.breathe_out
    assert breathe_config._hold_in > breathe_config.hold_in
    assert breathe_config._hold_out > breathe_config.hold_out


def test_breathe_config_calculates_duration_correctly():
    breathe_config = BreatheConfig(1, 2, 2, 2, 2)
    assert breathe_config.duration == 8
