from interactions import SlashCommandChoice

ROUND_CHOICES = [SlashCommandChoice(name=str(i), value=i) for i in range(1, 11)]
BREATHE_CHOICES = [SlashCommandChoice(name=str(i), value=i) for i in range(2, 11)]
HOLD_CHOICES = [SlashCommandChoice(name="None", value=0)] + BREATHE_CHOICES
