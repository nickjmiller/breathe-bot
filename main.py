import logging
import os

import interactions
from dotenv import load_dotenv
from interactions import (
    Client,
    Intents,
    Snowflake,
    listen,
)

from src.breathe_config import (
    Voice,
    breathe_config_cache,
)
from src.command import (
    breathe_in_option,
    breathe_out_option,
    hold_in_option,
    hold_out_option,
    round_option,
    voice_option,
)
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
@round_option
@voice_option
async def breathe_box(
    ctx: interactions.SlashContext, rounds: int = 5, voice: str = Voice.af
):
    logger.debug("Starting box breathing.")
    await channel_breathe(
        CURRENT_GUILDS,
        ctx,
        breathe_config_cache(
            voice=voice,
            breathe_in=4,
            hold_in=4,
            breathe_out=4,
            hold_out=4,
        ),
        rounds,
    )


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="478",
    sub_cmd_description="478 preset, 4 rounds of 4-7-8",
)
@round_option
@voice_option
async def breathe_478(
    ctx: interactions.SlashContext, rounds: int = 4, voice: str = Voice.af
):
    logger.debug("Starting 4-7-8 breathing.")
    await channel_breathe(
        CURRENT_GUILDS,
        ctx,
        breathe_config_cache(
            voice=voice,
            breathe_in=4,
            hold_in=7,
            breathe_out=8,
            hold_out=0,
        ),
        rounds,
    )


@interactions.slash_command(
    "breathe",
    description="Start guided breathing",
    sub_cmd_name="custom",
    sub_cmd_description="Define your own breathing exercise",
)
@round_option
@breathe_in_option
@hold_in_option
@breathe_out_option
@hold_out_option
@voice_option
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
        breathe_config_cache(
            breathe_in=breathe_in,
            hold_in=hold_in,
            breathe_out=breathe_out,
            hold_out=hold_out,
            voice=voice,
        ),
        rounds,
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
