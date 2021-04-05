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

class volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        @bot.command(name='volume')
        async def volume(ctx, volume: int):
            if ctx.voice_client is None:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Please connect to a voice channel'
                )

                return await ctx.send(embed=embed)


            elif ctx.voice_client is not None:
                if volume in range(0, 201):
                    try:
                        ctx.voice_client.source.volume = volume / 100

                        embed = discord.Embed(
                            title='Volume',
                            colour=discord.Colour.blue(),
                            description=f'Volume **{format(volume)}**'
                        )


                        return await ctx.send(embed=embed)
                    except:
                        pass

                else:

                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='That is louder than the music goes!'
                    )

                    return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(volume(bot))