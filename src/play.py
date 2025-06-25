import asyncio
from contextlib import asynccontextmanager

from interactions import (
    TYPE_VOICE_CHANNEL,
    Member,
    SlashContext,
    Snowflake,
    User,
    VoiceState,
)
from interactions.api.voice.audio import AudioVolume
from interactions.client.errors import VoiceNotConnected

from .breathe_config import BreatheConfig


class GuildAlreadyInUse(Exception):
    """Guild is already in use for the player."""

    pass


class MissingVoiceChannel(Exception):
    """Requester is not in a voice channel."""

    pass


def play_condition_check(
    current_guilds: set[Snowflake],
    author: Member | User,
) -> TYPE_VOICE_CHANNEL:
    try:
        channel = author.voice.channel
    except AttributeError:
        raise MissingVoiceChannel("Author is not in a voice channel.")
    if channel.guild.id in current_guilds:
        raise GuildAlreadyInUse(f"Guild {channel.guild} is already in use.")
    return channel


@asynccontextmanager
async def voice_channel_manager(
    channel: TYPE_VOICE_CHANNEL,
    voice_state: VoiceState | None,
    current_guilds: set[Snowflake],
):
    current_guilds.add(channel.guild.id)
    if not voice_state:
        await channel.connect()
    try:
        yield channel
    finally:
        try:
            await channel.disconnect()
        except VoiceNotConnected:
            pass
        finally:
            current_guilds.remove(channel.guild.id)


async def guided_breathe(voice_state: VoiceState, breathe_config: BreatheConfig):
    await voice_state.play(AudioVolume("assets/begin.wav"))
    for timer, audio in filter(
        lambda x: x[0] > 0, breathe_config.timer_audio_sequence()
    ):
        await voice_state.play(AudioVolume(audio))
        await asyncio.sleep(timer)
    await voice_state.play(AudioVolume("assets/done.ogg"))


async def channel_breathe(
    current_guilds: set[Snowflake],
    ctx: SlashContext,
    breathe_config: BreatheConfig,
):
    try:
        channel = play_condition_check(current_guilds, ctx.author)
    except MissingVoiceChannel:
        return await ctx.send(
            "You need to be in a voice channel to do the exercise!", delete_after=10
        )
    except GuildAlreadyInUse:
        return await ctx.send(
            "There is already a breathing exercise running!", delete_after=20
        )
    async with voice_channel_manager(channel, ctx.voice_state, current_guilds):
        await ctx.send(
            f"Starting guided breathing for {breathe_config.duration:.0f} seconds!",
            delete_after=100,
        )
        await guided_breathe(ctx.voice_state, breathe_config)
    await ctx.send("Done!", silent=True, delete_after=10)
