import pytest

from src.breathe_config import BreatheConfig, breathe_config_cache
from src.voice import Voice


def test_breathe_config_calculates_duration_correctly():
    breathe_config = BreatheConfig(breathe_in=2, hold_in=2, breathe_out=2, hold_out=2)
    assert breathe_config.round_duration == 8


@pytest.mark.parametrize(
    "config,expected",
    [
        (
            BreatheConfig(
                breathe_in=4, hold_in=4, breathe_out=4, hold_out=4, voice=Voice.af
            ),
            16,  # seconds
        ),
        (
            BreatheConfig(
                breathe_in=2, hold_in=2, breathe_out=3, hold_out=0, voice=Voice.af_quiet
            ),
            7,  # seconds
        ),
        (
            BreatheConfig(
                breathe_in=2, hold_in=0, breathe_out=4, hold_out=0, voice=Voice.am
            ),
            6,  # seconds
        ),
    ],
)
def test_breathe_config_generates_expected_round_audio(config, expected):
    # Round it to allow for small precision errors
    assert round(len(config._round_audio) / 1000) == expected
    assert round(len(config._round_audio_short) / 1000) == expected


def test_breathe_config_generates_expected_audio():
    breathe_config = BreatheConfig(
        breathe_in=4, hold_in=4, breathe_out=4, hold_out=4, voice=Voice.af_quiet
    )
    expected = 35  # Two rounds of 16 + duration of begin.wav
    assert round(len(breathe_config.audio(2)) / 1000) == expected


def test_breathe_config_cache_caches():
    assert breathe_config_cache(
        breathe_in=1, hold_in=1, breathe_out=1, hold_out=1, voice=Voice.af
    ) is breathe_config_cache(
        breathe_in=1, hold_in=1, breathe_out=1, hold_out=1, voice=Voice.af
    )
