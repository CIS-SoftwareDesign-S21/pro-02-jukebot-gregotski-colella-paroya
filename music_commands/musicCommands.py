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


# playlists = {}

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
        self.playlists = []
        self.totalPlaylists = []

        @bot.command(name='play', help='Plays a song')
        async def play(ctx, url: str = None):
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
                        filename = await YTDLSources.from_url(self.queue[0], loop=bot.loop)
                        voice_channel.play(
                            discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                        # voice_channel.play(filename, after=lambda e: print('Player error: %s' % e) if e else None)
                    await ctx.send('**Now playing:** {}'.format(filename))
                    # await ctx.send(f'**Now playing:** {filename.title}')
                    del (self.queue[0])
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

        @bot.command(name='remove', help='Removes song from queue')
        async def remove(ctx, number):
            try:
                if len(self.queue) != 0:
                    del (self.queue[int(number)])
                    await ctx.send("Song was deleted from queue")
                else:
                    await ctx.send("Queue is currently empty")
            except:
                pass

        @bot.command(name='view', help='Shows the queue')
        async def view(ctx):
            x = 0
            try:
                if len(self.queue) == 0:
                    await ctx.send("Your queue is currently empty")
                else:
                    while x <= len(self.queue):
                        filename = await YTDLSources.from_url(self.queue[x],
                                                              loop=bot.loop)
                        await ctx.send(f'**Your queue is now: ** ' + '[' + str(x) + '] ' + filename + '!')
                        x += 1
            except:
                pass

        @bot.command(name='viewplaylists', help='Shows all created playlists')
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

        @bot.command(name='create', help='Creates a playlist')
        async def create(ctx, playlist):

           # if self.totalPlaylists.__contains__(playlist):
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
          #  else:
          #      await ctx.send("Playlist already exists")

        @bot.command(name='addto', help='Add songs to playlist of songs')
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

        @bot.command(name='playfrom', help='Play a song from a playlist')
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
                            filename = await YTDLSources.from_url(self.playlists[num][0], loop=bot.loop)
                            voice_channel.play(
                                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                              #  x += 1
                            await ctx.send('**Now playing:** {}'.format(filename))
                except:
                    await ctx.send("Can't play song")

        @bot.command(name='removefrom', help='Removes song from playlist')
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

        @bot.command(name='delete', help='Deletes playlist')
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

        @bot.command(name='viewplaylist', help='Shows the playlist')
        async def viewplaylist(ctx, playlist):
            x = 0
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("Your playlist is currently empty")
                    else:
                        while x <= len(self.playlists[num]):
                            filename = await YTDLSources.from_url(self.playlists[num][x], loop=bot.loop)
                            await ctx.send(f'**Your playlist consists of: ** ' + '[' + str(x) + '] ' + filename + '!')
                            x += 1
            except:
                pass

        @bot.command(name='volume', help='Changes volume of currently playing')
        async def volume(ctx, volume: float):
            guild_to_audiocontroller = {}
            if ctx.voice_client is None:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Please connect to a voice channel'
                )

                return await ctx.send(embed=embed)

            elif ctx.voice_client is not None:
                if volume in range(0, 100):
                    try:
                        current_guild = ctx.message.guild
                        if current_guild is None:
                            await ctx.send_message("No guild")
                            return

                        guild_to_audiocontroller[current_guild].volume = volume
                        #   player = get_player(ctx)
                        #           ctx.voice_client.source.volume = volume / 100
                        #  player.volume = volume / 100
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
