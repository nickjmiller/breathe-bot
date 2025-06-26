import enum
from collections.abc import Generator
from dataclasses import dataclass
from enum import auto

VOICE_DIR = "assets/voices"


class Voice(enum.StrEnum):
    af = auto()
    am = auto()


DURATIONS = {
    Voice.af: {
        "in": 1.53,
        "hold": 1.35,
        "out": 1.48,
    },
    Voice.am: {
        "in": 1.30,
        "hold": 1.08,
        "out": 1.30,
    },
}


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
        durations = DURATIONS[self.voice]
        breathe_in = (
            self.breathe_in - durations["in"],
            f"{VOICE_DIR}/{self.voice}/in.wav",
        )
        hold_in = (
            self.hold_in - durations["hold"],
            f"{VOICE_DIR}/{self.voice}/hold.wav",
        )
        breathe_out = (
            self.breathe_out - durations["out"],
            f"{VOICE_DIR}/{self.voice}/out.wav",
        )
        hold_out = (
            self.hold_out - durations["hold"],
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
