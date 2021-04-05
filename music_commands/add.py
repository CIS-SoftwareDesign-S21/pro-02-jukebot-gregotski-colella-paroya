import discord
from discord.ext import commands
from collections import deque

class add(commands.Cog):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()

        @bot.command(name='add')
        async def addSong(ctx, url: str):
            connected = ctx.author.voice.channel

            if connected:
                self.queue.append(url)
                await ctx.send("Song added to queue")
                return
            else:
                await ctx.send("Could not add song to queue")



def setup(bot):
    bot.add_cog(add(bot))
