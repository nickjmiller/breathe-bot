import asyncio
import os
from collections import defaultdict

import interactions
from dotenv import load_dotenv
from interactions import Client, Intents, listen
from interactions.api.events import Component
from interactions.api.voice.audio import AudioVolume
from interactions.client.errors import VoiceNotConnected

from breathe_config import BreatheConfig
from components.duration_components import get_duration_components

load_dotenv()
bot = Client(intents=Intents.DEFAULT)


CHANNEL_MAP = defaultdict(BreatheConfig)


@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen(Component)
async def on_component(event: Component):
    ctx = event.ctx
    value = 0 if ctx.values[0] == "None" else int(ctx.values[0])
    setattr(CHANNEL_MAP[ctx.channel_id], f"_{ctx.custom_id}", value)
    await ctx.send("Updated!", silent=True, delete_after=1)


@interactions.slash_command(
    "breatheconf", description="Set up parameters for breathing"
)
async def breatheconf(ctx: interactions.SlashContext):
    await ctx.channel.send(
        "Configure",
        components=get_duration_components(),
        delete_after=60,
    )
    await ctx.send("Configure breathing options.", silent=True, delete_after=0.01)


@interactions.slash_command("breathe", description="Start box breathing")
async def play(ctx: interactions.SlashContext):
    breathe_config = CHANNEL_MAP[ctx.channel_id]
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.send(
            "You need to be in a voice channel to do the exercise!", delete_after=10
        )
        return
    if not ctx.voice_state:
        await channel.connect()
    await ctx.send(
        f"Starting box breathing for {breathe_config.duration:.0f} seconds!",
        delete_after=100,
    )
    await ctx.voice_state.play(AudioVolume("assets/begin.wav"))
    for i in range(breathe_config.iterations):
        if i == breathe_config.iterations - 1:
            await ctx.send("Last one!", delete_after=50)
        await ctx.voice_state.play_no_wait(AudioVolume("assets/in.wav"))
        await asyncio.sleep(breathe_config.breathe_in)
        if breathe_config.hold_in > 0:
            await ctx.voice_state.play_no_wait(AudioVolume("assets/hold.wav"))
            await asyncio.sleep(breathe_config.hold_in)
        await ctx.voice_state.play_no_wait(AudioVolume("assets/out.wav"))
        await asyncio.sleep(breathe_config.breathe_out)
        if breathe_config.hold_out > 0:
            await ctx.voice_state.play_no_wait(AudioVolume("assets/hold.wav"))
            await asyncio.sleep(breathe_config.hold_out)
    await ctx.voice_state.play(AudioVolume("assets/done.ogg"))
    try:
        await channel.disconnect()
    except VoiceNotConnected:
        pass


bot.start(os.getenv("BOT_SECRET"))
