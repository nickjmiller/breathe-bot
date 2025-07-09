from unittest.mock import ANY, AsyncMock, MagicMock

import pytest
from interactions.client.errors import VoiceNotConnected

from src.breathe_config import BreatheConfig
from src.play import (
    GuildAlreadyInUse,
    MissingVoiceChannel,
    channel_breathe,
    guided_breathe,
    play_condition_check,
    stop_guided_breathe,
    voice_channel_manager,
)


class TestVoiceChannelManager:
    @pytest.fixture
    def channel(self) -> AsyncMock:
        channel = AsyncMock()
        channel.guild.id = "guild"
        return channel

    @pytest.fixture
    def voice_state(self) -> MagicMock:
        return MagicMock()

    async def test_connects_and_disconnects_when_not_already_connected(self, channel):
        current_guilds = set()

        channel.connect.assert_not_awaited()
        channel.disconnect.assert_not_awaited()
        assert channel.guild.id not in current_guilds
        async with voice_channel_manager(channel, None, current_guilds) as voice_state:
            assert channel.guild.id in current_guilds
            channel.connect.assert_awaited_once()
            assert voice_state is channel.voice_state

        assert channel.guild.id not in current_guilds
        channel.disconnect.assert_awaited_once()
        channel.connect.assert_awaited_once()

    async def test_does_not_connect_when_already_connected(self, channel, voice_state):
        current_guilds = set()

        channel.connect.assert_not_awaited()
        channel.disconnect.assert_not_awaited()
        assert channel.guild.id not in current_guilds
        async with voice_channel_manager(
            channel, voice_state, current_guilds
        ) as voice_state:
            assert channel.guild.id in current_guilds
            channel.connect.assert_not_awaited()
            assert voice_state is channel.voice_state

        assert channel.guild.id not in current_guilds
        channel.disconnect.assert_awaited_once()
        channel.connect.assert_not_awaited()

    async def test_ignores_disconnect_error(self, channel, voice_state):
        current_guilds = set()
        channel.disconnect.side_effect = VoiceNotConnected()

        assert channel.guild.id not in current_guilds
        async with voice_channel_manager(
            channel, voice_state, current_guilds
        ) as voice_state:
            assert channel.guild.id in current_guilds
            assert voice_state is channel.voice_state

        assert channel.guild.id not in current_guilds
        channel.disconnect.assert_awaited_once()


class TestGuidedBreathe:
    async def test_plays_expected_audio(self):
        breathe_config = BreatheConfig()
        voice_state = AsyncMock()
        await guided_breathe(voice_state, breathe_config, 2)
        assert voice_state.play.await_count == 2


class TestPlayConditionCheck:
    @pytest.fixture()
    def guild_id(self) -> str:
        return "guild"

    @pytest.fixture()
    def author(self, guild_id: str) -> MagicMock:
        author = MagicMock()
        author.voice.channel.guild.id = guild_id
        return author

    def test_returns_channel(self, author):
        assert play_condition_check(set(), author) == author.voice.channel

    def test_raises_when_voice_channel_missing(self, author):
        del author.voice.channel
        with pytest.raises(MissingVoiceChannel):
            play_condition_check(set(), author)

    def test_raises_when_already_in_set(self, author, guild_id):
        current_guilds = set()
        current_guilds.add(guild_id)
        with pytest.raises(GuildAlreadyInUse):
            play_condition_check(current_guilds, author)


class TestChannelBreathe:
    @pytest.fixture()
    def channel(self) -> AsyncMock:
        channel = AsyncMock()
        channel.guild.id = "guild"
        return channel

    @pytest.fixture()
    def ctx(self, channel) -> AsyncMock:
        mock_ctx = AsyncMock()
        author = MagicMock()
        author.voice.channel = channel
        mock_ctx.author = author

        def send(message, **kwargs):
            return message

        mock_ctx.send.side_effect = send
        return mock_ctx

    async def test_no_channel_returns_missing_voice_channel(self, ctx):
        del ctx.author.voice.channel
        response = await channel_breathe(set(), ctx, BreatheConfig(), 1)
        assert response == "You need to be in a voice channel to do the exercise!"

    async def test_existing_channel_returns_channel_already_in_use(self, ctx, channel):
        current_guilds = set()
        current_guilds.add(channel.guild.id)
        response = await channel_breathe(current_guilds, ctx, BreatheConfig(), 1)
        assert response == "There is already a breathing exercise running!"

    async def test_no_voice_after_connect_returns_unexpected_error(self, ctx):
        ctx.author.voice.channel.voice_state = None
        response = await channel_breathe(set(), ctx, BreatheConfig(), 1)
        assert response == "There was an issue starting the exercise!"

    async def test_returns_none_when_complete(self, ctx):
        response = await channel_breathe(set(), ctx, BreatheConfig(), 1)
        assert response is None
        assert ctx.send.await_count == 2


class TestStopGuidedBreathe:
    async def test_sends_error_when_no_exercise_found(self):
        ctx = AsyncMock()
        ctx.voice_state = None
        await stop_guided_breathe(ctx)
        ctx.send.assert_awaited_once_with(
            "No current breathing exercises found in this server!", delete_after=ANY
        )

    async def test_disconnects(self):
        ctx = AsyncMock()

        await stop_guided_breathe(ctx)
        ctx.voice_state.channel.disconnect.assert_awaited_once()
