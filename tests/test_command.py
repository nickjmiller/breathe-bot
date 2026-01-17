import pytest

from command import BREATHE_CHOICES, HOLD_CHOICES, ROUND_CHOICES


@pytest.mark.parametrize(
    "choices,expected",
    [
        (
            ROUND_CHOICES,
            [
                ("1", 1),
                ("2", 2),
                ("3", 3),
                ("4", 4),
                ("5", 5),
                ("6", 6),
                ("7", 7),
                ("8", 8),
                ("9", 9),
                ("10", 10),
            ],
        ),
        (
            BREATHE_CHOICES,
            [
                ("2", 2),
                ("3", 3),
                ("4", 4),
                ("5", 5),
                ("6", 6),
                ("7", 7),
                ("8", 8),
                ("9", 9),
                ("10", 10),
            ],
        ),
        (
            HOLD_CHOICES,
            [
                ("None", 0),
                ("2", 2),
                ("3", 3),
                ("4", 4),
                ("5", 5),
                ("6", 6),
                ("7", 7),
                ("8", 8),
                ("9", 9),
                ("10", 10),
            ],
        ),
    ],
)
def test_choices_contain_expected_values(choices, expected):
    [(choice.name, choice.value) for choice in choices] == expected
