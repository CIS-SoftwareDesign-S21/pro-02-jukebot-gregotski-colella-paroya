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


class resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='resume')
        async def resume(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                await ctx.send("The bot was not playing anything before this. Use play_song command")


def setup(bot):
    bot.add_cog(resume(bot))
