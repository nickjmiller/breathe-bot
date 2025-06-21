from collections.abc import Generator
from dataclasses import dataclass


@dataclass(init=True)
class BreatheConfig:
    rounds: int = 5
    breathe_in: int = 4
    hold_in: int = 4
    breathe_out: int = 4
    hold_out: int = 4

    @property
    def duration(self) -> float:
        return self.rounds * (
            self.breathe_in + self.breathe_out + self.hold_in + self.hold_out
        )

    def timer_audio_sequence(self) -> Generator[tuple[float, str]]:
        breathe_in = (self.breathe_in - 1.53, "assets/in.wav")
        hold_in = (self.hold_in - 1.35, "assets/hold.wav")
        breathe_out = (self.breathe_out - 1.48, "assets/out.wav")
        hold_out = (self.hold_out - 1.35, "assets/hold.wav")
        for _ in range(self.rounds):
            yield breathe_in
            yield hold_in
            yield breathe_out
            yield hold_out
