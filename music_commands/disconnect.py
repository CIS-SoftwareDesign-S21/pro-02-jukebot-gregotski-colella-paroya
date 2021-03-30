import discord
from discord.ext import commands


class disconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='disconnect')
        async def disconnect(ctx):
            await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(disconnect(bot))
