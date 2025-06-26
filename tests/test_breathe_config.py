import pytest

from src.breathe_config import BreatheConfig


def test_breathe_config_calculates_duration_correctly():
    breathe_config = BreatheConfig(1, 2, 2, 2, 2)
    assert breathe_config.duration == 8


def test_breathe_config_generates_timer_sequence():
    breathe_config = BreatheConfig(2, 4, 4, 4, 4)
    assert list(breathe_config.timer_audio_sequence()) == [
        (pytest.approx(2.47), "assets/voices/af/in.wav"),
        (pytest.approx(2.65), "assets/voices/af/hold.wav"),
        (pytest.approx(2.52), "assets/voices/af/out.wav"),
        (pytest.approx(2.65), "assets/voices/af/hold.wav"),
        (pytest.approx(2.47), "assets/voices/af/in.wav"),
        (pytest.approx(2.65), "assets/voices/af/hold.wav"),
        (pytest.approx(2.52), "assets/voices/af/out.wav"),
        (pytest.approx(2.65), "assets/voices/af/hold.wav"),
    ]
