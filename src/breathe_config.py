import enum
from collections.abc import Generator
from dataclasses import dataclass
from enum import auto

VOICE_DIR = "assets/voices"


@dataclass(frozen=True)
class Duration:
    breathe_in: float
    breathe_out: float
    hold: float


class Voice(enum.StrEnum):
    af = auto()
    am = auto()

    @property
    def display_name(self):
        match self:
            case Voice.af:
                return "American Female"
            case Voice.am:
                return "American Male"


def get_durations(voice: Voice):
    match voice:
        case Voice.af:
            return Duration(breathe_in=1.53, breathe_out=1.48, hold=1.35)
        case Voice.am:
            return Duration(breathe_in=1.58, breathe_out=1.53, hold=1.33)


@dataclass(init=True)
class BreatheConfig:
    rounds: int = 5
    breathe_in: int = 4
    hold_in: int = 4
    breathe_out: int = 4
    hold_out: int = 4
    voice: Voice = Voice.af

    @property
    def duration(self) -> float:
        return self.rounds * (
            self.breathe_in + self.breathe_out + self.hold_in + self.hold_out
        )

    @property
    def begin_audio(self) -> str:
        return f"{VOICE_DIR}/{self.voice}/begin.wav"

    def timer_audio_sequence(self) -> Generator[tuple[float, str]]:
        durations = get_durations(self.voice)
        breathe_in = (
            self.breathe_in - durations.breathe_in,
            f"{VOICE_DIR}/{self.voice}/in.wav",
        )
        hold_in = (
            self.hold_in - durations.hold,
            f"{VOICE_DIR}/{self.voice}/hold.wav",
        )
        breathe_out = (
            self.breathe_out - durations.breathe_out,
            f"{VOICE_DIR}/{self.voice}/out.wav",
        )
        hold_out = (
            self.hold_out - durations.hold,
            f"{VOICE_DIR}/{self.voice}/hold.wav",
        )
        for _ in range(self.rounds):
            yield breathe_in
            yield hold_in
            yield breathe_out
            yield hold_out


class BreathePresets(enum.Enum):
    BOX_BREATHE = BreatheConfig(5, 4, 4, 4, 4)
    FOUR_SEVEN_EIGHT = BreatheConfig(4, 4, 7, 8, 0)
