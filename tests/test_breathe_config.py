import pytest

from src.breathe_config import BreatheConfig, Voice, breathe_config_cache, get_durations


def test_voice_has_display_name():
    for voice in Voice:
        assert voice.display_name is not None


def test_voice_has_durations():
    for voice in Voice:
        assert get_durations(voice) is not None


def test_breathe_config_calculates_duration_correctly():
    breathe_config = BreatheConfig(2, 2, 2, 2)
    assert breathe_config.round_duration == 8


@pytest.mark.parametrize(
    "config,expected",
    [
        (
            BreatheConfig(4, 4, 4, 4, Voice.af),
            16,  # seconds
        ),
        (
            BreatheConfig(2, 0, 4, 0, Voice.am),
            6,  # seconds
        ),
    ],
)
def test_breathe_config_generates_expected_round_audio(config, expected):
    assert round(len(config._round_audio) / 1000) == expected


def test_breathe_config_generates_expected_audio():
    breathe_config = BreatheConfig(4, 4, 4, 4, voice=Voice.af_quiet)
    expected = 35  # Two rounds of 16 + duration of begin.wav
    assert round(len(breathe_config.audio(2)) / 1000) == expected


def test_breathe_config_cache_caches():
    assert breathe_config_cache(
        breathe_in=1, hold_in=1, breathe_out=1, hold_out=1, voice=Voice.af
    ) is breathe_config_cache(
        breathe_in=1, hold_in=1, breathe_out=1, hold_out=1, voice=Voice.af
    )
