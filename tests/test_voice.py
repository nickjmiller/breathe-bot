from voice import Voice, get_durations


def test_voice_has_display_name():
    for voice in Voice:
        assert voice.display_name is not None


def test_voice_has_durations():
    for voice in Voice:
        assert get_durations(voice) is not None
