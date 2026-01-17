import asyncio
import logging
import os
import tempfile
from contextlib import asynccontextmanager
from typing import Optional, Set

import discord

from breathe_config import BreatheConfig

logger = logging.getLogger(__name__)


VoiceChannelType = discord.VoiceChannel | discord.StageChannel


class BreathingManager:
    def __init__(self):
        self._active_guilds: Set[int] = set()

    def _validate_request(
        self, interaction: discord.Interaction
    ) -> Optional[VoiceChannelType]:
        if (
            not isinstance(interaction.user, discord.Member)
            or not interaction.user.voice
        ):
            return None

        channel = interaction.user.voice.channel
        if not channel or interaction.guild_id in self._active_guilds:
            return None

        return channel

    async def _generate_audio_file(self, config: BreatheConfig, rounds: int) -> str:
        loop = asyncio.get_running_loop()

        def _write():
            fd, path = tempfile.mkstemp(suffix=".ogg")
            try:
                audio = config.audio(rounds)
                with os.fdopen(fd, "wb") as f:
                    audio.export(f, format="ogg")
            except Exception:
                os.close(fd)
                os.remove(path)
                raise
            return path

        return await loop.run_in_executor(None, _write)

    async def _play_until_done(
        self, vc: discord.VoiceClient, source: discord.AudioSource
    ):
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        def after(error):
            if not future.done():
                loop.call_soon_threadsafe(future.set_result, error)

        vc.play(source, after=after)
        await future

    @asynccontextmanager
    async def _voice_context(self, channel: VoiceChannelType):
        guild_id = channel.guild.id
        self._active_guilds.add(guild_id)

        vc = channel.guild.voice_client
        if not vc:
            vc = await channel.connect()
        elif vc.channel != channel:
            await vc.move_to(channel)  # ty:ignore[unresolved-attribute]
        if not isinstance(vc, discord.VoiceClient):
            self._active_guilds.discard(guild_id)
            raise RuntimeError("Could not establish a valid VoiceClient connection.")
        try:
            yield vc
        finally:
            if vc.is_connected():
                await vc.disconnect(force=True)
            self._active_guilds.discard(guild_id)

    async def start_session(
        self, interaction: discord.Interaction, config: BreatheConfig, rounds: int
    ):
        target_channel = self._validate_request(interaction)

        if not target_channel:
            msg = (
                "You must be in a voice channel."
                if hasattr(interaction.user, "voice") and not interaction.user.voice
                else "Session already running."
            )
            return await interaction.response.send_message(
                msg, ephemeral=True, delete_after=10
            )

        await interaction.response.defer()

        temp_path = None
        try:
            async with self._voice_context(target_channel) as vc:
                duration = config.round_duration * rounds
                await interaction.followup.send(
                    f"Starting guided breathing for {duration:.0f} seconds!"
                )

                temp_path = await self._generate_audio_file(config, rounds)
                await self._play_until_done(vc, discord.FFmpegPCMAudio(temp_path))

                if vc.is_connected():
                    await self._play_until_done(
                        vc, discord.FFmpegPCMAudio("assets/done.ogg")
                    )
                    await interaction.followup.send("Done!")

        except Exception:
            logger.exception("Error during breathing session")
            await interaction.followup.send(
                "An error occurred during the session.", ephemeral=True
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    async def stop_session(self, interaction: discord.Interaction):
        if not interaction.guild or not interaction.guild.voice_client:
            return await interaction.response.send_message(
                "No active session found.", delete_after=10, ephemeral=True
            )

        await interaction.guild.voice_client.disconnect(force=True)
        # Context manager in start_session handles cleanup
        await interaction.response.send_message(
            "Session stopped.", delete_after=10, ephemeral=True
        )
