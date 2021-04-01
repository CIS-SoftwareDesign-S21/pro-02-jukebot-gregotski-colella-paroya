import discord

from discord.ext import commands
import os

TOKEN = open("token.txt", "r").read()

bot = commands.Bot(command_prefix='!')

if __name__ == '__main__':
    for filename in os.listdir('./music_commands'):
        try:
            # loading the different commands but skips __init__ since it's just blank
            if filename != '__init__.py' and filename.endswith('.py'):
                bot.load_extension(f'music_commands.{filename[:-3]}')
        except Exception as error:
            print("Error: not able to load commands")
            print(error)
    print("Commands successfully loaded!")


@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot is online!")


bot.run(TOKEN)