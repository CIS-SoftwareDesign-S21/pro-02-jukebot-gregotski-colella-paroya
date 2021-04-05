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

        @bot.command(name='play', help='Plays a song')
        async def play(ctx, url: str=None):
            connected = ctx.author.voice.channel
            if url is not None:
                self.queue.appendleft(url)

         #   for s in self.queue:
         #       print(s)
        #    while len(self.queue) > 0:
            if connected:
                try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        filename = await YTDLSources.from_url(self.queue[0],loop=bot.loop)#self.queue.popleft(), loop=bot.loopself.queue[0],loop=bot.loop)
                        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                        # voice_channel.play(filename, after=lambda e: print('Player error: %s' % e) if e else None)
                    await ctx.send('**Now playing:** {}'.format(filename))
                    # await ctx.send(f'**Now playing:** {filename.title}')
                    del(self.queue[0])
                except:
                    await ctx.send("Can't play song")



        @bot.command(name='pause', help='Pauses currently playing song')
        async def pause(ctx):
            # try:
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                await ctx.send("The bot is not playing anything at the moment.")
            # except:
            await ctx.send("Can't stop playing song")

        @bot.command(name='resume', help='Continues playing paused song')
        async def resume(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                await ctx.send("The bot was not playing anything before this. Use play_song command")

        @bot.command(name='stop', help='Stops the song')
        async def stop(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await ctx.send("The bot is not playing anything at the moment.")

        @bot.command(name='add', help='Add songs to queue of songs')
        async def add(ctx, url: str):
            connected = ctx.author.voice.channel

            if connected:
                self.queue.append(url)
                await ctx.send("Song added to queue")
                return
            else:
                await ctx.send("Could not add song to queue")


        @bot.command(name='volume', help='Changes volume of currently playing')
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
                        ctx.voice_client.source.volume = float(volume) / 100

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
