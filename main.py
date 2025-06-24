import os
from collections import defaultdict
from dataclasses import replace

import interactions
from dotenv import load_dotenv
from interactions import (
    Client,
    Intents,
    OptionType,
    SlashCommandChoice,
    listen,
    slash_option,
)
from interactions.api.events import Component

from src.breathe_config import BOX_BREATHE, FOUR_SEVEN_EIGHT, BreatheConfig
from src.components.duration_components import get_duration_components
from src.play import (
    channel_play,
)

load_dotenv()
bot = Client(intents=Intents.DEFAULT)


CHANNEL_MAP = defaultdict(BreatheConfig)
CURRENT_CHANNELS = set()
ROUND_CHOICES = [SlashCommandChoice(name=str(i), value=i) for i in range(1, 10)]


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen(Component)
async def on_component(event: Component):
    ctx = event.ctx
    value = 0 if ctx.values[0] == "None" else int(ctx.values[0])
    setattr(CHANNEL_MAP[ctx.channel_id], ctx.custom_id, value)
    await ctx.send("Updated!", silent=True, delete_after=1)


@interactions.slash_command(
    "breatheconf", description="Set up default parameters for breathing"
)
async def breatheconf(ctx: interactions.SlashContext):
    await ctx.channel.send(
        "Configure",
        components=get_duration_components(),
        delete_after=60,
    )
    await ctx.send("Configure breathing options.", silent=True, delete_after=0.01)


@interactions.slash_command(
    "breathe", description="Start guided breathing using the channel default parameters"
)
async def breathe(ctx: interactions.SlashContext):
    breathe_config = CHANNEL_MAP[ctx.channel_id]
    await channel_play(CURRENT_CHANNELS, ctx, breathe_config)


@interactions.slash_command(
    "breathe_preset",
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
async def breathe_preset_box(ctx: interactions.SlashContext, rounds: int = 5):
    await channel_play(CURRENT_CHANNELS, ctx, replace(BOX_BREATHE, rounds=rounds))


@interactions.slash_command(
    "breathe_preset",
    description="Start guided breathing",
    sub_cmd_name="478",
    sub_cmd_description="Guided breathing, 4 rounds of 4-7-8",
)
@slash_option(
    name="rounds",
    description="How many rounds to breathe, default is 4",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=ROUND_CHOICES,
)
async def breathe_preset_478(ctx: interactions.SlashContext, rounds: int = 4):
    await channel_play(CURRENT_CHANNELS, ctx, replace(FOUR_SEVEN_EIGHT, rounds=rounds))


bot.start(os.getenv("BOT_SECRET"))
