import enum
from dataclasses import dataclass
from enum import auto
from functools import cache, cached_property

from pydub import AudioSegment

VOICE_DIR = "assets/voices"


@dataclass(frozen=True, kw_only=True)
class Duration:
    breathe_in: float
    breathe_out: float
    hold: float


class Voice(enum.StrEnum):
    af = auto()
    af_quiet = auto()
    am = auto()

    @property
    def display_name(self):
        match self:
            case Voice.af:
                return "American Female"
            case Voice.af_quiet:
                return "American Female (quiet)"
            case Voice.am:
                return "American Male"


def get_durations(voice: Voice):
    match voice:
        case Voice.af:
            return Duration(breathe_in=1.53, breathe_out=1.48, hold=1.35)
        case Voice.af_quiet:
            return Duration(breathe_in=1.63, breathe_out=1.7, hold=1.3)
        case Voice.am:
            return Duration(breathe_in=1.58, breathe_out=1.53, hold=1.33)


@dataclass(frozen=True, kw_only=True)
class BreatheConfig:
    breathe_in: int = 4
    hold_in: int = 4
    breathe_out: int = 4
    hold_out: int = 4
    voice: Voice = Voice.af

    @cached_property
    def _round_audio(self):
        durations = get_durations(self.voice)

        audio = AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/in.wav")
        audio += AudioSegment.silent((self.breathe_in - durations.breathe_in) * 1000)
        if self.hold_in > 0:
            audio += AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/hold.wav")
            audio += AudioSegment.silent((self.hold_in - durations.hold) * 1000)
        audio += AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/out.wav")
        audio += AudioSegment.silent((self.breathe_out - durations.breathe_out) * 1000)
        if self.hold_out > 0:
            audio += AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/hold.wav")
            audio += AudioSegment.silent((self.hold_out - durations.hold) * 1000)
        return audio

    def audio(self, rounds: int) -> AudioSegment:
        return AudioSegment.from_wav(f"{VOICE_DIR}/{self.voice}/begin.wav") + (
            self._round_audio * rounds
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
