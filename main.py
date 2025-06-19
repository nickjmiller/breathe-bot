import asyncio
import interactions
import os

from collections import defaultdict

from dotenv import load_dotenv
from interactions.api.events import Component
from interactions.api.voice.audio import AudioVolume
from interactions.client.errors import VoiceNotConnected
from interactions import Client, Intents, listen

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
    setattr(CHANNEL_MAP[ctx.channel_id], f"_{ctx.custom_id}", int(ctx.values[0]))
    await ctx.send("Updated!", silent=True, delete_after=0.1)


@interactions.slash_command(
    "breatheconf", description="Set up parameters for breathing"
)
async def breatheconf(ctx: interactions.SlashContext):
    await ctx.channel.send(
        "Configure",
        components=get_duration_components(),
        delete_after=60,
    )
    await ctx.send("Configure breathing options.", silent=True, delete_after=0.1)


@interactions.slash_command("breathe", description="Start box breathing")
async def play(ctx: interactions.SlashContext):
    breathe_config = CHANNEL_MAP[ctx.channel_id]
    if not ctx.voice_state:
        await ctx.author.voice.channel.connect()
    await ctx.send(
        f"Starting box breathing for {breathe_config.duration:.0f} seconds!",
        delete_after=100,
    )
    await ctx.voice_state.play(AudioVolume("assets/begin.wav"))
    for i in range(breathe_config.iterations):
        if i == breathe_config.iterations - 1:
            await ctx.send("Last one!", delete_after=50)
        await ctx.voice_state.play(AudioVolume("assets/in.wav"))
        await asyncio.sleep(breathe_config.breathe_in)
        await ctx.voice_state.play(AudioVolume("assets/hold.wav"))
        await asyncio.sleep(breathe_config.hold_in)
        await ctx.voice_state.play(AudioVolume("assets/out.wav"))
        await asyncio.sleep(breathe_config.breathe_out)
        await ctx.voice_state.play(AudioVolume("assets/hold.wav"))
        await asyncio.sleep(breathe_config.hold_out)
    await ctx.voice_state.play(AudioVolume("assets/done.ogg"))
    try:
        await ctx.author.voice.channel.disconnect()
    except VoiceNotConnected:
        pass


bot.start(os.getenv("BOT_SECRET"))
