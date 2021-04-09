import asyncio
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import youtube_dl
from collections import deque
import helperFunctions
import helpMessages

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
        title = data['title']
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename,  title


class MusicCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()
        self.history = deque()
        self.playlists = []
        self.totalPlaylists = []

        @bot.command(name='play', description=helpMessages.PLAY_LONG, help=helpMessages.PLAY_SHORT)
        async def play(ctx, url: str = None):
            connected = ctx.author.voice.channel

            # check if song is already playing
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                voice_client.stop()

            # if argument given
            if url is not None:
                # if argument not a youtube link, convert
                if not ("watch?v=" in url):
                    url = helperFunctions.convert_to_link(url)
                    # if converting to youtube link was unsuccessful
                    if not ("watch?v=" in url):
                        await ctx.send("Can't find result from Youtube")
                        return

                # add url to queue and history list
                self.queue.appendleft(url)
                self.history.append(url)

            if connected:
                try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        filename, title = await YTDLSources.from_url(self.queue[0], loop=bot.loop)
                        # self.queue.popleft(), loop=bot.loopself.queue[0],loop=bot.loop)
                        # voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                        voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg", source=filename))
                        # voice_channel.play(filename, after=lambda e: print('Player error: %s' % e) if e else None)
                    await ctx.send('**Now playing:** {}'.format(title))

                    del (self.queue[0])
                except:
                    await ctx.send("Can't play song")

        @bot.command(name='view', help=helpMessages.VIEW)
        async def view(ctx):

            embed = discord.Embed(
                title="Queue:",
                color=discord.Color.blue()
            )

            x = 0
            try:
                if len(self.queue) == 0:
                    await ctx.send("Your queue is currently empty")
                else:
                    while x <= len(self.queue):
                        filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
                        # add another field for artist, another for song title,another for time
                        embed.add_field(name="Track", value=title, inline=True)
                        # await ctx.send(embed=embed) #ctx.send(f'**Your queue is now: ** ' + '[' + str(x) + '] ' + filename + '!')
                        x += 1
                    await ctx.send(embed=embed)
            except:
                await ctx.send(embed=embed)

        @bot.command(name='remove', help=helpMessages.REMOVE)
        async def remove(ctx, number):
            try:
                if len(self.queue) != 0:
                    del (self.queue[int(number)])
                    await ctx.send("Song was deleted from queue")
                else:
                    await ctx.send("Queue is currently empty")
            except:
                pass

        @bot.command(name='pause', help=helpMessages.PAUSE)
        async def pause(ctx):
            # try:
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                await ctx.send("The bot is not playing anything at the moment.")
            # except:#
            await ctx.send("Can't stop playing song")

        @bot.command(name='resume', help=helpMessages.RESUME)
        async def resume(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                await ctx.send("The bot was not playing anything before this. Use play_song command")

        @bot.command(name='stop', help=helpMessages.STOP)
        async def stop(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                await ctx.send("The bot is not playing anything at the moment.")

        @bot.command(name='add', help=helpMessages.ADD)
        async def add(ctx, url: str):
            connected = ctx.author.voice.channel

            if not ("watch?v=" in url):
                url = helperFunctions.convert_to_link(url)
                if not ("watch?v=" in url):
                    await ctx.send("Can't find result from Youtube")
                    return

            if connected:
                self.queue.append(url)
                await ctx.send("Song added to queue")
                return
            else:
                await ctx.send("Could not add song to queue")

        @bot.command(name='viewplaylists', help=helpMessages.VIEW_PLAYLISTS)
        async def viewplaylists(ctx):
            x = 0
            try:
                if len(self.totalPlaylists) == 0:
                    await ctx.send("There are no playlists created")
                else:
                    while x <= len(self.playlists):
                        await ctx.send(f'**Playlist: ** ' + self.totalPlaylists[x])
                        x += 1
            except:
                pass

        @bot.command(name='create', help=helpMessages.CREATE)
        async def create(ctx, playlist):
            if any(playlist in s for s in self.totalPlaylists):
                await ctx.send("Playlist already exists")

            else:
                try:
                    self.totalPlaylists.append(playlist)
                    playlist = [playlist]
                    x = 0
                    while len(playlist) > 0:
                        playlist.__delitem__(x)
                        x += 1
                    self.playlists.append(playlist)
                    await ctx.send("Playlist created!")
                except:
                    await ctx.send("Could not create playlist")

        @bot.command(name='addto', help=helpMessages.ADD_TO)
        async def addto(ctx, playlist, url: str):
            connected = ctx.author.voice.channel
            if connected:
                try:
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
                        # if playlist in self.playlists:
                        self.playlists[num].append(url)
                        await ctx.send("Song added to playlist")
                        return
                except:
                    await ctx.send("Could not add song to playlist")

        @bot.command(name='playfrom', help=helpMessages.PLAY_FROM)
        async def playfrom(ctx, playlist: str):
            connected = ctx.author.voice.channel
            if connected:
                try:
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
                        async with ctx.typing():
                            x = 0
                           # while len(self.playlists[num]) > 0:
                            filename, title = await YTDLSources.from_url(self.playlists[num][0], loop=bot.loop)
                            voice_channel.play(
                                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                              #  x += 1
                            await ctx.send('**Now playing:** {}'.format(title))
                except:
                    await ctx.send("Can't play song")

        @bot.command(name='removefrom', help=helpMessages.REMOVE_FROM)
        async def removefrom(ctx, playlist, number: str):
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) != 0:
                        del (self.playlists[num][int(number)])
                        await ctx.send("Song was deleted from playlist")
                else:
                    await ctx.send("Playlist is currently empty")
            except:
                pass

        @bot.command(name='delete', help=helpMessages.DELETE)
        async def delete(ctx, playlist):
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    del (self.playlists[num])
                    del (self.totalPlaylists[num])
                    await ctx.send("Playlist deleted")
                else:
                    await ctx.send("Playlist does not exist")
            except:
                pass

        @bot.command(name='viewplaylist', help=helpMessages.VIEW_PLAYLIST)
        async def viewplaylist(ctx, playlist):
            x = 0
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("Your playlist is currently empty")
                    else:
                        while x <= len(self.playlists[num]):
                            filename, title = await YTDLSources.from_url(self.playlists[num][x], loop=bot.loop)
                            await ctx.send(f'**Your playlist consists of: ** ' + '[' + str(x) + '] ' + title + '!')
                            x += 1
            except:
                pass

        @bot.command(name='volume', help=helpMessages.VOLUME)
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
