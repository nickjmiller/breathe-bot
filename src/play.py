import logging
import tempfile
from contextlib import asynccontextmanager

from interactions import (
    TYPE_VOICE_CHANNEL,
    ActiveVoiceState,
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


logger = logging.getLogger(__name__)


def play_condition_check(
    current_guilds: set[Snowflake],
    author: Member | User,
) -> TYPE_VOICE_CHANNEL:
    try:
        channel = author.voice.channel  # ty: ignore[possibly-unbound-attribute]
    except AttributeError:
        logger.info(
            f"Attempted to start breathing exercise without a voice channel, {author.id}"
        )
        raise MissingVoiceChannel("Author is not in a voice channel.")
    if channel.guild.id in current_guilds:
        logger.info(
            f"Attempted to start breathing exercise while already playing in a channel, guild={channel.guild.id}"
        )
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
        yield channel.voice_state
    finally:
        try:
            await channel.disconnect()
        except VoiceNotConnected:
            logger.warning("Bot already disconnected before disconnect called.")
            pass
        finally:
            current_guilds.remove(channel.guild.id)


async def guided_breathe(
    voice_state: ActiveVoiceState, breathe_config: BreatheConfig, rounds: int
):
    with tempfile.NamedTemporaryFile(suffix=".ogg") as tmpfile:
        logger.info(f"Created temporary file at: {tmpfile.name}")
        breathe_config.audio(rounds).export(tmpfile, format="ogg")
        await voice_state.play(AudioVolume(tmpfile.name))
    await voice_state.play(AudioVolume("assets/done.ogg"))


async def channel_breathe(
    current_guilds: set[Snowflake],
    ctx: SlashContext,
    breathe_config: BreatheConfig,
    rounds: int,
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
    async with voice_channel_manager(
        channel, ctx.voice_state, current_guilds
    ) as voice_state:
        await ctx.send(
            f"Starting guided breathing for {(breathe_config.round_duration * rounds):.0f} seconds!",
            delete_after=100,
        )
        if voice_state is None:
            logger.error(
                f"Voice state was none after connecting to the channel, {ctx=}"
            )
            return await ctx.send(
                "There was an issue starting the exercise!", delete_after=20
            )
        await guided_breathe(voice_state, breathe_config, rounds)
    await ctx.send("Done!", silent=True, delete_after=10)


async def stop_guided_breathe(ctx: SlashContext):
    if ctx.voice_state is None:
        logger.info(
            f"Tried stopping a guided breathing with no voice context, {ctx.guild_id=}"
        )
        return await ctx.send(
            "No current breathing exercises found in this server!", delete_after=10
        )
    await ctx.voice_state.channel.disconnect()
    await ctx.send("Stopped!", delete_after=10)
