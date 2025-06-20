from enum import StrEnum, auto

from interactions import StringSelectMenu, spread_to_rows


class SelectId(StrEnum):
    rounds = auto()
    breathe_in = auto()
    hold_in = auto()
    breathe_out = auto()
    hold_out = auto()


nums = [str(i) for i in range(3, 11)]
rounds = StringSelectMenu(
    "1",
    "2",
    *nums,
    placeholder="How many repetitions?",
    min_values=1,
    max_values=1,
    custom_id=SelectId.rounds,
)
breathe_in = StringSelectMenu(
    *nums,
    placeholder="How long to inhale?",
    min_values=1,
    max_values=1,
    custom_id=SelectId.breathe_in,
)
hold_in = StringSelectMenu(
    "None",
    *nums,
    placeholder="How long to hold after inhaling?",
    min_values=1,
    max_values=1,
    custom_id=SelectId.hold_in,
)
breathe_out = StringSelectMenu(
    *nums,
    placeholder="How long to exhale?",
    min_values=1,
    max_values=1,
    custom_id=SelectId.breathe_out,
)
hold_out = StringSelectMenu(
    "None",
    *nums,
    placeholder="How long to hold after exhaling?",
    min_values=1,
    max_values=1,
    custom_id=SelectId.hold_out,
)


def get_duration_components():
    return spread_to_rows(rounds, breathe_in, hold_in, breathe_out, hold_out)
