import asyncio
import os
import random

import discord
from discord import app_commands

TOKEN = os.environ["DISCORD_TOKEN"]  # never hardcode your token

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()  # registers slash commands with Discord
    print(f"Logged in as {client.user}")


@tree.command(name="roll", description="Roll a die")
@app_commands.describe(sides="Number of sides (default 6)")
async def roll(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("A die needs at least 2 sides!")
        return
    await interaction.response.send_message(f"You rolled a **{random.randint(1, sides)}** (d{sides})")


@tree.command(name="8ball", description="Ask the magic 8-ball")
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = ["Yes.", "No.", "Maybe.", "Definitely.", "Ask again later.", "Very doubtful."]
    await interaction.response.send_message(f"🎱 *{question}*\n{random.choice(answers)}")


@tree.command(name="remind", description="Get a reminder after some minutes")
@app_commands.describe(minutes="How many minutes to wait", message="What to remind you about")
async def remind(interaction: discord.Interaction, minutes: int, message: str):
    await interaction.response.send_message(f"Okay, I'll remind you in {minutes} min.")
    await asyncio.sleep(minutes * 60)
    await interaction.followup.send(f"{interaction.user.mention} Reminder: {message}")


client.run(TOKEN)
