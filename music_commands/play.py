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
from collections import deque
from music_commands import add

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


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='play')
        async def play(ctx, url: str):
            connected = ctx.author.voice.channel
            if connected:
              try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        filename = await YTDLSources.from_url(url, loop=bot.loop)
                        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                    await ctx.send('**Now playing:** {}'.format(filename))
              except:
                    await ctx.send("Can't play song")
<<<<<<< HEAD
      #        if self.queue:
      #            print (len(self.queue))
      #            print (self.queue[0])
      #            await play(self.queue.popleft())
=======
              if self.queue:
                  print (len(add.queue))
                  print (add.queue[0])
                  await play(add.queue.popleft())
>>>>>>> 2f0f1a1cec26c24b4be4e151d901e406710ed4d8


def setup(bot):
    bot.add_cog(play(bot))

