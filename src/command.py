from interactions import OptionType, SlashCommandChoice, slash_option

from src.breathe_config import Voice

MAX_DURATION = 10
ROUND_CHOICES = [SlashCommandChoice(name=str(i), value=i) for i in range(1, 11)]
BREATHE_CHOICES = [
    SlashCommandChoice(name=str(i), value=i) for i in range(2, MAX_DURATION + 1)
]
HOLD_CHOICES = [SlashCommandChoice(name="None", value=0)] + BREATHE_CHOICES
VOICE_CHOICES = [
    SlashCommandChoice(name=voice.display_name, value=voice) for voice in Voice
]

round_option = slash_option(
    name="rounds",
    description="How many rounds",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=ROUND_CHOICES,
)
breathe_in_option = slash_option(
    name="breathe_in",
    description="How long to breathe in",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=BREATHE_CHOICES,
)
hold_in_option = slash_option(
    name="hold_in",
    description="How long to hold in",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=HOLD_CHOICES,
)
breathe_out_option = slash_option(
    name="breathe_out",
    description="How long to breathe out",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=BREATHE_CHOICES,
)
hold_out_option = slash_option(
    name="hold_out",
    description="How long to hold out",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=HOLD_CHOICES,
)
voice_option = slash_option(
    "voice",
    description="Voice for the guided exercise",
    required=False,
    opt_type=OptionType.STRING,
    choices=VOICE_CHOICES,
)
