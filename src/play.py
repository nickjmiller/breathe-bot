import asyncio
from contextlib import asynccontextmanager

from interactions import TYPE_VOICE_CHANNEL, Member, User, VoiceState
from interactions.api.voice.audio import AudioVolume
from interactions.client.errors import VoiceNotConnected

from .breathe_config import BreatheConfig


class ChannelAlreadyInUse(Exception):
    """Channel is already in use for the player."""

    pass


class MissingVoiceChannel(Exception):
    """Requester is not in a voice channel."""

    pass


def play_condition_check(
    current_channels: set[TYPE_VOICE_CHANNEL],
    author: Member | User,
) -> TYPE_VOICE_CHANNEL:
    try:
        channel = author.voice.channel
    except AttributeError:
        raise MissingVoiceChannel("Author is not in a voice channel.")
    if channel in current_channels:
        raise ChannelAlreadyInUse(f"Channel {channel} is already in use.")
    return channel


@asynccontextmanager
async def voice_channel_manager(
    channel: TYPE_VOICE_CHANNEL,
    voice_state: VoiceState | None,
    current_channels: set[TYPE_VOICE_CHANNEL],
):
    current_channels.add(channel)
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
            current_channels.remove(channel)


async def box_breathe(voice_state: VoiceState, breathe_config: BreatheConfig):
    await voice_state.play(AudioVolume("assets/begin.wav"))
    for timer, audio in filter(
        lambda x: x[0] > 0, breathe_config.timer_audio_sequence()
    ):
        await voice_state.play(AudioVolume(audio))
        await asyncio.sleep(timer)
    await voice_state.play(AudioVolume("assets/done.ogg"))
