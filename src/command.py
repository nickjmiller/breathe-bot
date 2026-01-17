from discord import app_commands
from discord.app_commands import Choice

from voice import Voice

MAX_DURATION = 10


# Helper to create Choice objects
def make_choice(name, value) -> Choice:
    return app_commands.Choice(name=str(name), value=value)


ROUND_CHOICES = [make_choice(i, i) for i in range(1, 11)]

BREATHE_CHOICES = [make_choice(i, i) for i in range(2, MAX_DURATION + 1)]

HOLD_CHOICES = [make_choice("None", 0)] + BREATHE_CHOICES

VOICE_CHOICES = [
    app_commands.Choice(name=voice.display_name, value=voice.value) for voice in Voice
]
