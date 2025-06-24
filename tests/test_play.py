from collections.abc import Generator
from unittest import mock
from unittest.mock import AsyncMock, MagicMock

import pytest
from interactions.client.errors import VoiceNotConnected

from src.breathe_config import BreatheConfig
from src.play import (
    ChannelAlreadyInUse,
    MissingVoiceChannel,
    channel_play,
    guided_breathe,
    play_condition_check,
    voice_channel_manager,
)


class TestVoiceChannelManager:
    @pytest.fixture
    def channel(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def voice_state(self) -> MagicMock:
        return MagicMock()

    async def test_connects_and_disconnects_when_not_already_connected(self, channel):
        current_channels = set()

        channel.connect.assert_not_awaited()
        channel.disconnect.assert_not_awaited()
        assert channel not in current_channels
        async with voice_channel_manager(
            channel, None, current_channels
        ) as yielded_channel:
            assert channel in current_channels
            channel.connect.assert_awaited_once()
            assert yielded_channel is channel

        assert channel not in current_channels
        channel.disconnect.assert_awaited_once()
        channel.connect.assert_awaited_once()

    async def test_does_not_connect_when_already_connected(self, channel, voice_state):
        current_channels = set()

        channel.connect.assert_not_awaited()
        channel.disconnect.assert_not_awaited()
        assert channel not in current_channels
        async with voice_channel_manager(
            channel, voice_state, current_channels
        ) as yielded_channel:
            assert channel in current_channels
            channel.connect.assert_not_awaited()
            assert yielded_channel is channel

        assert channel not in current_channels
        channel.disconnect.assert_awaited_once()
        channel.connect.assert_not_awaited()

    async def test_ignores_disconnect_error(self, channel, voice_state):
        current_channels = set()
        channel.disconnect.side_effect = VoiceNotConnected()

        assert channel not in current_channels
        async with voice_channel_manager(
            channel, voice_state, current_channels
        ) as yielded_channel:
            assert channel in current_channels
            assert yielded_channel is channel

        assert channel not in current_channels
        channel.disconnect.assert_awaited_once()


class TestGuidedBreathe:
    @pytest.fixture
    def mock_sleep(self) -> Generator[AsyncMock]:
        with mock.patch("src.play.asyncio.sleep", new_callable=AsyncMock) as m:
            yield m

    async def test_guided_breathe_in_sequence(self, mock_sleep):
        breathe_config = BreatheConfig(1, 2, 2, 2, 2)
        voice_state = AsyncMock()
        await guided_breathe(voice_state, breathe_config)
        assert voice_state.play.await_count == 6
        mock_sleep.assert_has_awaits(
            [
                mock.call(pytest.approx(0.47)),
                mock.call(pytest.approx(0.65)),
                mock.call(pytest.approx(0.52)),
                mock.call(pytest.approx(0.65)),
            ],
            any_order=False,
        )

    async def test_guided_breathe_filters_zero_timers(self, mock_sleep):
        breathe_config = BreatheConfig(1, 2, 0, 2, 0)
        voice_state = AsyncMock()
        await guided_breathe(voice_state, breathe_config)
        assert voice_state.play.await_count == 4
        mock_sleep.assert_has_awaits(
            [
                mock.call(pytest.approx(0.47)),
                mock.call(pytest.approx(0.52)),
            ],
            any_order=False,
        )


class TestPlayConditionCheck:
    @pytest.fixture()
    def channel(self) -> str:
        return "test_channel"

    @pytest.fixture()
    def author(self, channel: str) -> MagicMock:
        author = MagicMock()
        author.voice.channel = channel
        return author

    def test_returns_channel(self, author, channel):
        assert play_condition_check(set(), author) == channel

    def test_raises_when_voice_channel_missing(self, author):
        del author.voice.channel
        with pytest.raises(MissingVoiceChannel):
            play_condition_check(set(), author)

    def test_raises_when_already_in_set(self, author, channel):
        current_channels = set()
        current_channels.add(channel)
        with pytest.raises(ChannelAlreadyInUse):
            play_condition_check(current_channels, author)


class TestChannelPlay:
    @pytest.fixture()
    def channel(self) -> AsyncMock:
        return AsyncMock()

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

    @pytest.fixture
    def mock_sleep(self) -> Generator[AsyncMock]:
        with mock.patch("src.play.asyncio.sleep", new_callable=AsyncMock) as m:
            yield m

    async def test_returns_missing_voice_channel(self, ctx):
        del ctx.author.voice.channel
        response = await channel_play(set(), ctx, BreatheConfig())
        assert response == "You need to be in a voice channel to do the exercise!"

    async def test_returns_channel_already_in_use(self, ctx, channel):
        current_channels = set()
        current_channels.add(channel)
        response = await channel_play(current_channels, ctx, BreatheConfig())
        assert response == "There is already a breathing exercise running!"

    async def test_returns_done_when_complete(self, ctx, mock_sleep):
        response = await channel_play(set(), ctx, BreatheConfig())
        assert response is None
        assert ctx.send.await_count == 2
