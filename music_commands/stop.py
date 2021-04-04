
import discord
from discord.ext import commands
import asyncio
import youtube_dl
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl


class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='stop', help='Stops the song')
        async def stop(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await ctx.send("The bot is not playing anything at the moment.")


def setup(bot):
    bot.add_cog(stop(bot))

