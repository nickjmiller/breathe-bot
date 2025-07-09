from dataclasses import dataclass
from functools import cache, cached_property

from pydub import AudioSegment

from .voice import VOICE_DIR, Voice, get_durations


@dataclass(frozen=True, kw_only=True)
class BreatheConfig:
    breathe_in: int = 4
    hold_in: int = 4
    breathe_out: int = 4
    hold_out: int = 4
    voice: Voice = Voice.af

    def generate_round_audio(self, short=False):
        durations = get_durations(self.voice)

        audio = AudioSegment.from_wav(
            f"{VOICE_DIR}/{self.voice}/in{'_short' if short else ''}.wav"
        )
        audio += AudioSegment.silent(
            (
                self.breathe_in
                - (durations.breathe_in_short if short else durations.breathe_in)
            )
            * 1000
        )
        if self.hold_in > 0:
            audio += AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/hold.wav")
            audio += AudioSegment.silent((self.hold_in - durations.hold) * 1000)
        audio += AudioSegment.from_wav(
            f"{VOICE_DIR}/{self.voice}/out{'_short' if short else ''}.wav"
        )
        audio += AudioSegment.silent(
            (
                self.breathe_out
                - (durations.breathe_out_short if short else durations.breathe_out)
            )
            * 1000
        )
        if self.hold_out > 0:
            audio += AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/hold.wav")
            audio += AudioSegment.silent((self.hold_out - durations.hold) * 1000)
        return audio

    @cached_property
    def _round_audio(self):
        return self.generate_round_audio(short=False)

    @cached_property
    def _round_audio_short(self):
        return self.generate_round_audio(short=True)

    def audio(self, rounds: int) -> AudioSegment:
        return (
            AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/begin.wav")
            + self._round_audio
            + self._round_audio_short * (rounds - 1)
        )

    @cached_property
    def round_duration(self) -> float:
        return self.breathe_in + self.breathe_out + self.hold_in + self.hold_out


@cache
def breathe_config_cache(
    *, breathe_in: int, hold_in: int, breathe_out: int, hold_out: int, voice: Voice
):
    return BreatheConfig(
        breathe_in=breathe_in,
        hold_in=hold_in,
        breathe_out=breathe_out,
        hold_out=hold_out,
        voice=voice,
    )
