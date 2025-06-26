import logging
import os
from dataclasses import replace

import interactions
from dotenv import load_dotenv
from interactions import (
    Client,
    Intents,
    OptionType,
    Snowflake,
    listen,
    slash_option,
)

from src.breathe_config import BreatheConfig, BreathePresets, Voice
from src.command import BREATHE_CHOICES, HOLD_CHOICES, ROUND_CHOICES, VOICE_CHOICES
from src.play import (
    channel_breathe,
    stop_guided_breathe,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

load_dotenv()
bot = Client(intents=Intents.DEFAULT)


CURRENT_GUILDS: set[Snowflake] = set()


@listen()
async def on_ready():
    logger.info("Ready")


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
@slash_option(
    "voice",
    description="Voice for the guided exercise",
    required=False,
    opt_type=OptionType.STRING,
    choices=VOICE_CHOICES,
)
async def breathe_box(
    ctx: interactions.SlashContext, rounds: int = 5, voice: str = Voice.af
):
    logger.debug("Starting box breathing.")
    await channel_breathe(
        CURRENT_GUILDS,
        ctx,
        replace(BreathePresets.BOX_BREATHE.value, rounds=rounds, voice=voice),
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
@slash_option(
    "voice",
    description="Voice for the guided exercise",
    required=False,
    opt_type=OptionType.STRING,
    choices=VOICE_CHOICES,
)
async def breathe_478(
    ctx: interactions.SlashContext, rounds: int = 4, voice: str = Voice.af
):
    logger.debug("Starting 4-7-8 breathing.")
    await channel_breathe(
        CURRENT_GUILDS,
        ctx,
        replace(BreathePresets.FOUR_SEVEN_EIGHT.value, rounds=rounds, voice=voice),
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
@slash_option(
    "voice",
    description="Voice for the guided exercise",
    required=False,
    opt_type=OptionType.STRING,
    choices=VOICE_CHOICES,
)
async def breathe_custom(
    ctx: interactions.SlashContext,
    rounds: int,
    breathe_in: int,
    hold_in: int,
    breathe_out: int,
    hold_out: int,
    voice: str = Voice.af,
):
    logger.debug(
        f"Starting custom breathing: {rounds=} {breathe_in=} {hold_in=} {breathe_out=} {hold_out=} {voice=}"
    )
    await channel_breathe(
        CURRENT_GUILDS,
        ctx,
        BreatheConfig(
            rounds=rounds,
            breathe_in=breathe_in,
            hold_in=hold_in,
            breathe_out=breathe_out,
            hold_out=hold_out,
            voice=voice,
        ),
    )


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="stop",
    sub_cmd_description="Stop the current exercise",
)
async def breathe_stop(ctx: interactions.SlashContext):
    logger.debug(f"Stopping breathing exercise in {ctx.guild_id}")
    await stop_guided_breathe(ctx)


bot.start(os.getenv("BOT_SECRET"))
