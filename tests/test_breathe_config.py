import pytest

from src.breathe_config import BreatheConfig, Voice


def test_breathe_config_calculates_duration_correctly():
    breathe_config = BreatheConfig(1, 2, 2, 2, 2)
    assert breathe_config.duration == 8


@pytest.mark.parametrize(
    "config,expected",
    [
        (
            BreatheConfig(2, 4, 4, 4, 4, Voice.af),
            [
                (pytest.approx(2.47), "assets/voices/af/in.wav"),
                (pytest.approx(2.65), "assets/voices/af/hold.wav"),
                (pytest.approx(2.52), "assets/voices/af/out.wav"),
                (pytest.approx(2.65), "assets/voices/af/hold.wav"),
                (pytest.approx(2.47), "assets/voices/af/in.wav"),
                (pytest.approx(2.65), "assets/voices/af/hold.wav"),
                (pytest.approx(2.52), "assets/voices/af/out.wav"),
                (pytest.approx(2.65), "assets/voices/af/hold.wav"),
            ],
        ),
        (
            BreatheConfig(1, 4, 4, 4, 4, Voice.am),
            [
                (pytest.approx(2.42), "assets/voices/am/in.wav"),
                (pytest.approx(2.67), "assets/voices/am/hold.wav"),
                (pytest.approx(2.47), "assets/voices/am/out.wav"),
                (pytest.approx(2.67), "assets/voices/am/hold.wav"),
            ],
        ),
    ],
)
def test_breathe_config_generates_timer_sequence(config, expected):
    assert list(config.timer_audio_sequence()) == expected
