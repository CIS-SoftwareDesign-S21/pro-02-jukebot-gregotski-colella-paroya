import discord
from discord.ext import commands
import asyncio
import youtube_dl
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

class pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='pause')
        async def pause(ctx):
           # try:
                voice_client = ctx.message.guild.voice_client
                if voice_client.is_playing():
                    await voice_client.pause()
                else:
                    await ctx.send("The bot is not playing anything at the moment.")
            #except:
                await ctx.send("Can't stop playing song")

def setup(bot):
    bot.add_cog(pause(bot))