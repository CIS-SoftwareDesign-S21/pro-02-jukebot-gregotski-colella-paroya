import discord
from discord.ext import commands

class ServerCommands(commands.Cog):

    # Initialization
    def __init__(self, bot):
        self.bot = bot

        # Command to connect bot to voice channel (as of right now, user has to be
        # in channel to connect the bot)
        @bot.command(name='connect', help='Connects to voice channel')
        async def connect(msg):
            if msg.author.voice:
                connected = msg.author.voice.channel
                await connected.connect()
            else:
                await msg.send("Please connect to a voice channel to use this command.")

        @bot.command(name='disconnect', help='Disconnects from voice channel')
        async def disconnect(ctx):
            await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(ServerCommands(bot))
