import discord
from discord.ext import commands


class connect(commands.Cog):
    # Initialization
    def __init__(self, bot):
        self.bot = bot

        # Command to connect bot to voice channel (as of right now, user has to be
        # in channel to connect the bot)
        @bot.command(name='connect')
        async def connect(msg):
            if(msg.author.voice):
                connected = msg.author.voice.channel
                await connected.connect()
            else:
                await msg.send("Please connect to a voice channel to use this command.")


def setup(bot):
    bot.add_cog(connect(bot))
