from dataclasses import dataclass


@dataclass(init=True)
class BreatheConfig:
    _iterations: int = 5
    _breathe_in: int = 4
    _hold_in: int = 4
    _breathe_out: int = 4
    _hold_out: int = 4

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def breathe_in(self) -> float:
        # Subtract the duration of the audio file
        return self._breathe_in - 1.53

    @property
    def hold_in(self) -> float:
        # Subtract the duration of the audio file
        return self._hold_in - 1.35

    @property
    def breathe_out(self) -> float:
        # Subtract the duration of the audio file
        return self._breathe_out - 1.53

    @property
    def hold_out(self) -> float:
        # Subtract the duration of the audio file
        return self._hold_out - 1.35

    @property
    def duration(self) -> float:
        return self._iterations * (
            self._breathe_in + self._breathe_out + self._hold_in + self._hold_out
        )
