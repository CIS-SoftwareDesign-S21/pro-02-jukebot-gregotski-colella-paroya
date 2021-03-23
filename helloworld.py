import discord
from discord.ext import commands
import os

# Credentials

TOKEN = open("token.txt", "r").read()

# Creating the Bot + command prefix
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))


# Command

@bot.command()
async def hello_world(msg):
    await msg.send("Hello World!")

# Running the bot
bot.run(TOKEN)