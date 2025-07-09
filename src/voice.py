import enum
from dataclasses import dataclass
from enum import auto

VOICE_DIR = "assets/voices"


@dataclass(frozen=True, kw_only=True)
class Duration:
    breathe_in: float
    breathe_in_short: float
    breathe_out: float
    breathe_out_short: float
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
            return Duration(
                breathe_in=1.53,
                breathe_in_short=1.28,
                breathe_out=1.48,
                breathe_out_short=1.25,
                hold=1.35,
            )
        case Voice.af_quiet:
            return Duration(
                breathe_in=1.63,
                breathe_in_short=1.25,
                breathe_out=1.7,
                breathe_out_short=1.23,
                hold=1.3,
            )
        case Voice.am:
            return Duration(
                breathe_in=1.58,
                breathe_in_short=1.25,
                breathe_out=1.53,
                breathe_out_short=1.2,
                hold=1.33,
            )
