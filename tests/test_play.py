from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest

from breathe_config import BreatheConfig
from play import BreathingManager


class TestBreathingManagerContext:
    @pytest.fixture
    def manager(self):
        return BreathingManager()

    @pytest.fixture
    def guild(self):
        guild = MagicMock(spec=discord.Guild)
        guild.id = 123
        guild.voice_client = None
        return guild

    @pytest.fixture
    def channel(self, guild) -> AsyncMock:
        channel = AsyncMock(spec=discord.VoiceChannel)
        channel.guild = guild
        return channel

    async def test_connects_and_disconnects_when_not_already_connected(
        self, manager, channel
    ):
        vc = AsyncMock(spec=discord.VoiceClient)
        vc.channel = channel
        channel.connect.return_value = vc

        async with manager._voice_context(channel) as voice_client:
            assert 123 in manager._active_guilds
            channel.connect.assert_awaited_once()
            assert voice_client is vc

        assert 123 not in manager._active_guilds
        vc.disconnect.assert_awaited_once()

    async def test_uses_existing_vc_if_present(self, manager, channel, guild):
        vc = AsyncMock(spec=discord.VoiceClient)
        vc.channel = channel
        guild.voice_client = vc

        async with manager._voice_context(channel) as voice_client:
            assert 123 in manager._active_guilds
            channel.connect.assert_not_awaited()
            assert voice_client is vc

        assert 123 not in manager._active_guilds
        vc.disconnect.assert_awaited_once()


@patch("play.discord.FFmpegPCMAudio")
class TestStartSession:
    @pytest.fixture
    def manager(self):
        return BreathingManager()

    @pytest.fixture
    def interaction(self) -> AsyncMock:
        interaction = AsyncMock(spec=discord.Interaction)
        interaction.response.send_message = AsyncMock()
        interaction.response.defer = AsyncMock()
        interaction.followup.send = AsyncMock()
        interaction.is_expired.return_value = False

        guild = MagicMock(spec=discord.Guild)
        guild.id = 123
        guild.voice_client = None
        interaction.guild = guild
        interaction.guild_id = 123

        channel = AsyncMock(spec=discord.VoiceChannel)
        channel.guild = guild

        author = MagicMock(spec=discord.Member)
        author.voice = MagicMock()
        author.voice.channel = channel
        interaction.user = author

        vc = MagicMock(spec=discord.VoiceClient)
        vc.channel = channel
        vc.is_connected.return_value = True

        def mock_play(source, after):
            after(None)

        vc.play.side_effect = mock_play

        async def mock_connect():
            guild.voice_client = vc
            return vc

        channel.connect.side_effect = mock_connect

        return interaction

    async def test_successful_run(self, mock_ffmpeg, manager, interaction):
        with patch.object(manager, "_generate_audio_file", return_value="dummy.ogg"):
            await manager.start_session(interaction, BreatheConfig(), 1)

        interaction.response.defer.assert_awaited_once()
        assert interaction.followup.send.await_count >= 2

    async def test_no_channel_returns_error_message(
        self, mock_ffmpeg, manager, interaction
    ):
        interaction.user.voice = None
        await manager.start_session(interaction, BreatheConfig(), 1)
        interaction.response.send_message.assert_awaited_once()

    async def test_guild_already_active(self, mock_ffmpeg, manager, interaction):
        manager._active_guilds.add(123)

        await manager.start_session(interaction, BreatheConfig(), 1)

        interaction.response.send_message.assert_awaited_once()
        args, _ = interaction.response.send_message.call_args
        assert "Session already running" in args[0]
