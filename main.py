import os
from dataclasses import replace

import interactions
from dotenv import load_dotenv
from interactions import (
    Client,
    Intents,
    OptionType,
    listen,
    slash_option,
)

from src.breathe_config import BreatheConfig, BreathePresets
from src.command import BREATHE_CHOICES, HOLD_CHOICES, ROUND_CHOICES
from src.play import (
    channel_breathe,
)

load_dotenv()
bot = Client(intents=Intents.DEFAULT)


CURRENT_CHANNELS = set()


@listen()
async def on_ready():
    print("Ready")


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="box",
    sub_cmd_description="Box breathing, 5 rounds of 4-4-4-4",
)
@slash_option(
    name="rounds",
    description="How many rounds to breathe, default is 5",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=ROUND_CHOICES,
)
async def breathe_box(ctx: interactions.SlashContext, rounds: int = 5):
    await channel_breathe(
        CURRENT_CHANNELS, ctx, replace(BreathePresets.FOUR_SEVEN_EIGHT, rounds=rounds)
    )


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="478",
    sub_cmd_description="478 preset, 4 rounds of 4-7-8",
)
@slash_option(
    name="rounds",
    description="How many rounds to breathe, default is 4",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=ROUND_CHOICES,
)
async def breathe_478(ctx: interactions.SlashContext, rounds: int = 4):
    await channel_breathe(
        CURRENT_CHANNELS, ctx, replace(BreathePresets.FOUR_SEVEN_EIGHT, rounds=rounds)
    )


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="custom",
    sub_cmd_description="Define your own breathing exercise",
)
@slash_option(
    name="rounds",
    description="How many rounds",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=ROUND_CHOICES,
)
@slash_option(
    name="breathe_in",
    description="How long to breathe in",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=BREATHE_CHOICES,
)
@slash_option(
    name="hold_in",
    description="How long to hold in",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=HOLD_CHOICES,
)
@slash_option(
    name="breathe_out",
    description="How long to breathe out",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=BREATHE_CHOICES,
)
@slash_option(
    name="hold_out",
    description="How long to hold out",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=HOLD_CHOICES,
)
async def breathe_custom(
    ctx: interactions.SlashContext,
    rounds: int,
    breathe_in: int,
    hold_in: int,
    breathe_out: int,
    hold_out: int,
):
    await channel_breathe(
        CURRENT_CHANNELS,
        ctx,
        BreatheConfig(
            rounds=rounds,
            breathe_in=breathe_in,
            hold_in=hold_in,
            breathe_out=breathe_out,
            hold_out=hold_out,
        ),
    )


bot.start(os.getenv("BOT_SECRET"))
