import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from breathe_config import breathe_config_cache
from command import (
    BREATHE_CHOICES,
    HOLD_CHOICES,
    ROUND_CHOICES,
    VOICE_CHOICES,
)
from play import BreathingManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

manager = BreathingManager()


class BreatheBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.add_command(
            BreatheCommands(name="breathe", description="Start guided breathing")
        )

        await self.tree.sync()

    async def on_ready(self):
        logger.info(
            f"Ready: Logged in as {self.user} (ID: {self.user and self.user.id})"
        )


class BreatheCommands(app_commands.Group):
    """Group for breathing commands."""

    @app_commands.command(name="box", description="Box breathing, 5 rounds of 4-4-4-4")
    @app_commands.choices(rounds=ROUND_CHOICES, voice=VOICE_CHOICES)
    @app_commands.describe(rounds="How many rounds (default 5)", voice="Voice style")
    async def breathe_box(
        self, interaction: discord.Interaction, rounds: int = 5, voice: str = "af"
    ):
        logger.debug("Starting box breathing.")
        await manager.start_session(
            interaction,
            breathe_config_cache(
                voice=voice,
                breathe_in=4,
                hold_in=4,
                breathe_out=4,
                hold_out=4,
            ),
            rounds,
        )

    @app_commands.command(name="478", description="478 preset, 4 rounds of 4-7-8")
    @app_commands.choices(rounds=ROUND_CHOICES, voice=VOICE_CHOICES)
    async def breathe_478(
        self, interaction: discord.Interaction, rounds: int = 4, voice: str = "af"
    ):
        logger.debug("Starting 4-7-8 breathing.")
        await manager.start_session(
            interaction,
            breathe_config_cache(
                voice=voice,
                breathe_in=4,
                hold_in=7,
                breathe_out=8,
                hold_out=0,
            ),
            rounds,
        )

    @app_commands.command(
        name="custom", description="Define your own breathing exercise"
    )
    @app_commands.choices(
        rounds=ROUND_CHOICES,
        breathe_in=BREATHE_CHOICES,
        hold_in=HOLD_CHOICES,
        breathe_out=BREATHE_CHOICES,
        hold_out=HOLD_CHOICES,
        voice=VOICE_CHOICES,
    )
    async def breathe_custom(
        self,
        interaction: discord.Interaction,
        rounds: int,
        breathe_in: int,
        hold_in: int,
        breathe_out: int,
        hold_out: int,
        voice: str = "af",
    ):
        logger.debug(
            f"Starting custom breathing: {rounds=} {breathe_in=} {hold_in=} {breathe_out=} {hold_out=} {voice=}"
        )
        await manager.start_session(
            interaction,
            breathe_config_cache(
                breathe_in=breathe_in,
                hold_in=hold_in,
                breathe_out=breathe_out,
                hold_out=hold_out,
                voice=voice,
            ),
            rounds,
        )

    @app_commands.command(name="stop", description="Stop the current exercise")
    async def breathe_stop(self, interaction: discord.Interaction):
        logger.debug(f"Stopping breathing exercise in {interaction.guild_id}")
        await manager.stop_session(interaction)


if __name__ == "__main__":
    load_dotenv()
    bot = BreatheBot()
    bot.run(os.getenv("BOT_SECRET") or "")
