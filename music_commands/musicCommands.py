import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl
from collections import deque

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSources(discord.PCMVolumeTransformer, commands.Cog):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()

        @commands.command(name='play', help='Plays song')
        async def play(ctx, url: str):
            connected = ctx.author.voice.channel
            if connected:
                try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        filename = await YTDLSources.from_url(url, loop=bot.loop)
                        voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg", source=filename))
                    await ctx.send('**Now playing:** {}'.format(filename))
                except:
                    await ctx.send("Can't play song")

                #if self.queue:
                    #print(len(self.queue))
                    #print(self.queue[0])
                    #await play(self.queue.popleft())

        @commands.command(name='pause', help='Pauses currently playing song')
        async def pause(ctx):
            # try:
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                await ctx.send("The bot is not playing anything at the moment.")
            # except:
            await ctx.send("Can't stop playing song")

        @commands.command(name='resume', help='Continues playing paused song')
        async def resume(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                await ctx.send("The bot was not playing anything before this. Use play_song command")

        @commands.command(name='stop', help='Stops the song')
        async def stop(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await ctx.send("The bot is not playing anything at the moment.")

        @commands.command(name='add', help='Add songs to queue of songs')
        async def add(ctx, url: str):
            connected = ctx.author.voice.channel

            if connected:
                self.queue.append(url)
                await ctx.send("Song added to queue")
                return
            else:
                await ctx.send("Could not add song to queue")

        @commands.command(name='volume', help='Changes volume of currently playing')
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
    bot.add_cog(MusicCommands(bot))
