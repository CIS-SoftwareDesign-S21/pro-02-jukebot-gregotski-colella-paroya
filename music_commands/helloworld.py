import discord
from discord.ext import commands


class helloworld(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='helloworld')
        async def helloworld(msg):
            await msg.send("Hello World!")


def setup(bot):
    bot.add_cog(helloworld(bot))
