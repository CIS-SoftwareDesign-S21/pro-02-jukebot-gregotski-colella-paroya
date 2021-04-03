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
                        voice_channel.play(discord.FFmpegOpusAudio(executable="FFMPEG.exe", source=filename))##
                    await ctx.send('**Now playing:** {}'.format(filename))
                except:
                    await ctx.send("Can't play song")


def setup(bot):
    bot.add_cog(play(bot))

    #        server = ctx.message.server
    #        voice_client = bot.voice_client_in(server)
    #        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    #        players[server.id] = player
    #        player.start()

    #    songs = asyncio.Queue()
    #    play_next_song = asyncio.Event()

    #    players = {}
    #    queues = {}

    #     def check_queue(id):
    #        if queues[id] != []:
    #            player = queues[id].pop(0)
    #            players[id] = player
    #            player.start()

    #        song = os.path.isfile("song.mp3")
    #       try:
    #           if song:
    #               os.remove("song.mp3")
    #       except PermissionError:
    #           await ctx.send("Enter !stop to stop")
    #           return

    #    voice_channel = discord.utils.get(ctx.voice_client, name='General')

    #   voice = discord.utils.get(voice_channel, guild=ctx.guild)

    #   ydl_opts = {
    #       'format': 'bestaudio/best',
    #       'postprocessors': [{
    #           'key': 'FFmpegExtractAudio',
    #           'preferredcodec': 'mp3',
    #           'preferredequality': '192'
    #       }]
    #   }
    #   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #       ydl.download([url])
    #   for file in os.listdir("./"):
    #       if file.endswith(".mp3"):
    #           os.rename(file, "song.mp3")
    #   voice.play(discord.FFmpegPCMAudio("song.mp3"))

    #    try:
    #        server = ctx.message
    #        voice_client = bot.voice_client_in(server)
    #        player = await voice_client.create_ytdl_player(url)
    #        #  players[server.id] = player
    #        player.start()
    #    except:
    #        await ctx.send("The bot is not connected to a voice channel.")

    # audio = os.path.isfile("song.mp3")
    #  voiceChannel = discord.utils.get(msg.guild.voice_channels,name="General")
    #    await msg.play(msg, url)
    # server = msg.message
    # voice_client = bot.voice_client_in(server)
    # player = await voice_client.create_ytdl_player(url)
    #  players[server.id] = player
    # player.start()
