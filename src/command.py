from interactions import SlashCommandChoice

MAX_DURATION = 10
ROUND_CHOICES = [SlashCommandChoice(name=str(i), value=i) for i in range(1, 11)]
BREATHE_CHOICES = [
    SlashCommandChoice(name=str(i), value=i) for i in range(2, MAX_DURATION + 1)
]
HOLD_CHOICES = [SlashCommandChoice(name="None", value=0)] + BREATHE_CHOICES
VOICE_CHOICES = [
    SlashCommandChoice(name="American Male", value="am"),
    SlashCommandChoice(name="American Female", value="af"),
]
