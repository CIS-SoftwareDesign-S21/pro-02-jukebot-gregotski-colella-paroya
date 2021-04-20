import asyncio
import discord
import random
from discord.ext import commands
import csv
import youtube_dl
from collections import deque
import helperFunctions
import helpMessages
from discord.utils import get


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
        return filename, title


class MusicCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()
        self.history = deque()
        self.playlists = []
        self.totalPlaylists = []
        self.currentIndex = 0
        self.titles = []
        self.filenames = []
        self.retainedPlaylist = []
        self.retainedPlaylists = []
        self.reactions = ['⏸', '⏭', '🔁', '⏹']

        @bot.command(name="vote", help=helpMessages.VOTE)
        async def vote(ctx):
            if not ctx.message.guild.voice_client.is_playing():
                await ctx.send("Nothing playing to vote on")
                return
            msg = await ctx.send("Thoughts on the song? You've got 10 seconds to vote!")
            for emoji in self.reactions:
                await msg.add_reaction(emoji)

            channel = ctx.author.voice.channel
            numMembers = len(channel.members)

            #give time to vote
            await asyncio.sleep(10)

            msg = await ctx.channel.fetch_message(msg.id)
            pauseVotes = 0
            skipVotes = 0
            stopVotes= 0
            replayVotes = 0

            pauseVotes = msg.reactions[0].count
            skipVotes = msg.reactions[1].count
            replayVotes = msg.reactions[2].count
            stopVotes = msg.reactions[3].count

            print(skipVotes)
            if (skipVotes >= numMembers):
                await ctx.send("Skipping song")
                await skip(ctx)
            elif (pauseVotes >= numMembers):
                await ctx.send("Pausing song")
                await pause(ctx)
            elif (replayVotes >= numMembers):
                 await ctx.send("Replaying song!")
                 await replay(ctx)
            elif (stopVotes >= numMembers):
                await ctx.send("Stopping current song")
                await stop(ctx)
            else:
                await ctx.send("Not enough votes to pause, skip, replay, or stop")
                return

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
                    embed = discord.Embed(
                        title='Now Playing:',
                        colour=discord.Colour.blue()
                    )

                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    async with ctx.typing():
                        filename, title = await YTDLSources.from_url(self.queue[0], loop=bot.loop)
                        voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                                                  source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)               
                        voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg", source=filename))
                        embed.add_field(name="YouTube", value=title, inline=True)
                        # voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))embed.add_field(name="YouTube", value=title, inline=True)

                    del (self.queue[0])
                    return await ctx.send(embed=embed)
                    pass


                except:

                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Cannot play song'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='rewind', help=helpMessages.REWIND)
        async def rewind(ctx, num):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if len(self.history) == 0:
                    await ctx.send("**Can't rewind, there is nothing in your history**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Rewinding**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    filename, title = await YTDLSources.from_url(self.history[int(num) - 1], loop=bot.loop)
                    voice_channel.play(
                        discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                    # discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                    #                      source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
                    return
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not rewind to specified song')
                return await ctx.send(embed=embed)

        @bot.command(name='history', help=helpMessages.HISTORY)
        async def history(ctx):
            embed = discord.Embed(
                title="History:",
                color=discord.Color.dark_grey()
            )
            connected = ctx.author.voice.channel

            if connected:
                if len(self.history) == 0:
                    await ctx.send("**Your history is currently empty**")
                else:
                    x = 0
                    while x < len(self.history):
                        filename, title = await YTDLSources.from_url(self.history[x], loop=bot.loop)
                        embed.add_field(name="Song " + str(x + 1), value=title, inline=True)
                        x += 1
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not view history'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='replay', help=helpMessages.REPLAY)
        async def replay(ctx):

            embed = discord.Embed(
                title='Replaying:',
                colour=discord.Colour.blue()
            )
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_client = ctx.message.guild.voice_client

            try:
                filename, title = await YTDLSources.from_url(self.history[0], loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename), after=lambda e: self.history[0])
                # voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                #                                      source=filename))
                embed.add_field(name="YouTube", value=title, inline=True)
                await ctx.send(embed=embed)
                pass
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description="Can't replay song"
                )
            return await ctx.send(embed=embed)

        @bot.command(name='view', help=helpMessages.VIEW)
        async def view(ctx):

            embed = discord.Embed(
                title='Queue:',
                colour=discord.Colour.purple()
            )

            x = 0
            try:
                if len(self.queue) == 0:
                    await ctx.send("**Your queue is currently empty**")
                else:
                    while x < len(self.queue):
                        filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
                        embed.add_field(name="Song " + str(x + 1) + ": ", value=title, inline=True)
                        x += 1
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not view queue')
                return await ctx.send(embed=embed)

        @bot.command(name='skip', help=helpMessages.SKIP)
        async def skip(ctx):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )

            try:
                if len(self.queue) == 0:
                    await ctx.send("**Can't skip, there is nothing left in the queue**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Song was skipped**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    filename, title = await YTDLSources.from_url(self.queue[0], loop=bot.loop)
                    voice_channel.play(
                        discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                    #      discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg", source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
                # del (self.queue[0])
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not skip song')
                return await ctx.send(embed=embed)

        @bot.command(name='back', help=helpMessages.BACK)
        async def back(ctx):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if len(self.history) == 0:
                    await ctx.send("**Can't go back, there is nothing left in the queue**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Going back a song...**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client

                    filename, title = await YTDLSources.from_url(self.history[0], loop=bot.loop)
                    voice_channel.play(
                        discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                    # discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                    #   source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not go back in queue')
                return await ctx.send(embed=embed)

        @bot.command(name='skipfrom', help=helpMessages.SKIP_FROM)
        async def skipfrom(ctx, playlist):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("**Can't skip, playlist is empty**")
                    else:
                        voice_client = ctx.message.guild.voice_client
                        if voice_client.is_playing():
                            voice_client.stop()
                            await ctx.send("**Song was skipped**")
                            server = ctx.message.guild
                            voice_channel = server.voice_client
                            self.currentIndex += 1
                            filename, title = await YTDLSources.from_url(self.playlists[num][self.currentIndex],
                                                                         loop=bot.loop)
                            voice_channel.play(
                                # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                                discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                                       source=filename))

                            embed.add_field(name="YouTube", value=title, inline=True)
                            await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not skip song')
                return await ctx.send(embed=embed)

        @bot.command(name='shufflefrom', help=helpMessages.SHUFFLE_FROM)
        async def shufflefrom(ctx, playlist):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("**Can't shuffle empty playlist**")
                    else:
                        voice_client = ctx.message.guild.voice_client
                        if voice_client.is_playing():
                            voice_client.stop()
                        await ctx.send("**Playlist is now set to shuffle**")
                        server = ctx.message.guild
                        voice_channel = server.voice_client
                        filename, title = await YTDLSources.from_url(
                            self.playlists[num][random.randint(0, len(self.playlists[num]) - 1)], loop=bot.loop)
                        voice_channel.play(
                            # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                            discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                                   source=filename))
                        embed.add_field(name="YouTube", value=title, inline=True)
                        await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not shuffle through playlist')
                return await ctx.send(embed=embed)

        @bot.command(name='shuffle', help=helpMessages.SHUFFLE)
        async def shuffle(ctx):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if len(self.queue) == 0:
                    await ctx.send("**Can't shuffle empty queue**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Queue is now set to shuffle**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    filename, title = await YTDLSources.from_url(
                        self.queue[random.randint(0, len(self.queue) - 1)], loop=bot.loop)
                    voice_channel.play(
                        # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                        discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                               source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not shuffle through queue')
                return await ctx.send(embed=embed)

        @bot.command(name='backfrom', help=helpMessages.BACK_FROM)
        async def backfrom(ctx, playlist):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("**Can't go back, playlist is empty**")
                    else:
                        voice_client = ctx.message.guild.voice_client
                        if voice_client.is_playing():
                            voice_client.stop()
                            await ctx.send("**You went back one song**")
                            server = ctx.message.guild
                            voice_channel = server.voice_client
                            self.currentIndex -= 1
                            filename, title = await YTDLSources.from_url(self.playlists[num][self.currentIndex],
                                                                         loop=bot.loop)
                            voice_channel.play(
                                # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                                discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                                       source=filename))
                            embed.add_field(name="YouTube", value=title, inline=True)
                            await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not go back in playlist')
                return await ctx.send(embed=embed)

        @bot.command(name='remove', help=helpMessages.REMOVE)
        async def remove(ctx, index: int):
            try:
                if len(self.queue) != 0:
                    del (self.queue[index - 1])
                    return await ctx.send("**Song was deleted from queue**")
                else:
                    return await ctx.send("**Queue is currently empty**")
            except:
                pass

        @bot.command(name='pause', help=helpMessages.PAUSE)
        async def pause(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.pause()
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='The bot is not playing anything at the moment'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='resume', help=helpMessages.RESUME)
        async def resume(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_paused():
                await voice_client.resume()
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='The bot was not playing anything before this. Use !play command.'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='stop', help=helpMessages.STOP)
        async def stop(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_playing():
                await voice_client.stop()
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='The bot is not playing anything at the moment'
                )
                return await ctx.send(embed=embed)

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
                self.history.append(url)
                await ctx.send("**Song added to queue**")
                return
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not add song to queue'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='clear', help=helpMessages.CLEAR)
        async def clear(ctx):
            try:
                if len(self.queue) == 0:
                    return await ctx.send("**Queue is currently empty, cannot clear**")
                else:
                    self.queue.clear()
                    return await ctx.send("**Queue has been cleared!**")
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not clear queue'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='viewplaylists', help=helpMessages.VIEW_PLAYLISTS)
        async def viewplaylists(ctx):

            embed = discord.Embed(
                title="Playlists:",
                color=discord.Color.purple()
            )

            if 'allplaylists.csv' != None:

                file = open('allplaylists.csv', 'r')
                with file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        self.retainedPlaylists.append(row['playlists:'])
                        print(self.retainedPlaylists)

                    if self.retainedPlaylists is not None:
                        if self.totalPlaylists.__contains__(self.retainedPlaylists):
                            pass
                        else:
                            x = 0
                            while x < len(self.retainedPlaylists):
                                self.totalPlaylists.append(self.retainedPlaylists[x])
                                self.playlists.append(self.retainedPlaylists[x])
                                x+=1
            try:

                if len(self.totalPlaylists) == 0:
                    await ctx.send("**There are no playlists created**")
                else:
                    x = 0
                    while x < len(self.playlists):
                        embed.add_field(name="Playlist " + str(x + 1), value=self.totalPlaylists[x], inline=True)
                        x += 1
                    await ctx.send(embed=embed)
                    return
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Cannot view playlists'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='create', help=helpMessages.CREATE)
        async def create(ctx, playlist):
            if any(playlist in s for s in self.totalPlaylists):
                await ctx.send("**Playlist already exists**")

            else:
                try:
                    self.totalPlaylists.append(playlist)

                    file = open('playlists.csv', 'w')
                    with file:
                        writer = csv.DictWriter(file, fieldnames=self.totalPlaylists)
                        writer.writeheader()
                    file2 = open('allplaylists.csv','w')
                    with file2:
                        field = ['playlists:']
                        writing = csv.DictWriter(file2, fieldnames=field)
                        writing.writeheader()
                        writing2 = csv.writer(file2)
                        writing2.writerow(self.totalPlaylists)

                    playlist = [playlist]
                    x = 0
                    while len(playlist) > 0:
                        playlist.__delitem__(x)
                        x += 1
                    self.playlists.append(playlist)

                    await ctx.send("**Playlist created!**")
                except:

                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Could not create playlist'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='addto', help=helpMessages.ADD_TO)
        async def addto(ctx, playlist, url: str):
            connected = ctx.author.voice.channel

            if url is not None:
                # if argument not a youtube link, convert
                if not ("watch?v=" in url):
                    url = helperFunctions.convert_to_link(url)
                    # if converting to youtube link was unsuccessful
                    if not ("watch?v=" in url):
                        await ctx.send("Can't find result from Youtube")
                        return
            with open('playlists.csv', 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter='\n')
                file, title = await YTDLSources.from_url(url, loop=bot.loop)
                writer.writerow({playlist: title})

            if connected:
                try:
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
                        # if playlist in self.playlists:
                        self.playlists[num].append(url)
                        await ctx.send("**Song added to playlist**")
                        return
                except:
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Could not add song to playlist'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='playfrom', help=helpMessages.PLAY_FROM)
        async def playfrom(ctx, playlist: str):
            connected = ctx.author.voice.channel
            if connected:

                try:

                    embed = discord.Embed(
                        title='Now Playing:',
                        colour=discord.Colour.blue()
                    )

                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
                        async with ctx.typing():
                            filename, title = await YTDLSources.from_url(self.playlists[num][0], loop=bot.loop)
                            # voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                            voice_channel.play(
                                discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                                       source=filename))

                            embed.add_field(name="YouTube", value=title, inline=True)
                            await ctx.send(embed=embed)

                except:
                    pass
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Cannot play song from playlist'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='playsongfrom', help=helpMessages.PLAY_SONG_FROM)
        async def playsongfrom(ctx, playlist: str, song: str):
            connected = ctx.author.voice.channel
            if connected:
                try:
                    embed = discord.Embed(
                        title='Now Playing:',
                        colour=discord.Colour.blue()
                    )
                    self.currentIndex = int(song)
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
                        async with ctx.typing():
                            self.currentIndex = int(song) - 1
                            filename, title = await YTDLSources.from_url(self.playlists[num][self.currentIndex],
                                                                         loop=bot.loop)
                            voice_channel.play(
                                # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                                discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                                       source=filename))
                            embed.add_field(name="YouTube", value=title, inline=True)
                            await ctx.send(embed=embed)
                            pass

                except:
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Cannot play song from playlist'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='removefrom', help=helpMessages.REMOVE_FROM)
        async def removefrom(ctx, playlist, number: str):
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) != 0:
                        del (self.playlists[num][int(number)])
                        await ctx.send("**Song was deleted from playlist**")
                        return
                else:
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Playlist is already empty'
                    )
                    return await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Cannot view playlists'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='delete', help=helpMessages.DELETE)
        async def delete(ctx, playlist):
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    del (self.playlists[num])
                    del (self.totalPlaylists[num])
                    await ctx.send("**Playlist deleted**")
                    return
                else:
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Playlist does not exist'
                    )
                    return await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Cannot view playlist'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='viewplaylist', help=helpMessages.VIEW_PLAYLIST)
        async def viewplaylist(ctx, playlist):

            embed = discord.Embed(
                title=playlist,
                color=discord.Color.purple()
            )
            if 'playlists.csv' != None:
                file = open('playlists.csv','r')
                with file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        self.retained = (row[playlist])
                        if self.retained is not None:
                            self.playlists.append(self.retained)
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("**Your playlist is currently empty**")
                    else:
                        x = 0
                        while x < len(self.playlists[num]):
                            filename, title = await YTDLSources.from_url(self.playlists[num][x], loop=bot.loop)

                            embed.add_field(name="Song " + str(x + 1), value=title, inline=True)
                            x += 1
                        await ctx.send(embed=embed)
                        return
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Cannot view playlist'
                )
                return await ctx.send(embed=embed)

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
                if volume in range(0, 100):
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

        @bot.command(name='replay', help=helpMessages.REPLAY)
        async def replay(ctx):

            embed = discord.Embed(
                title='Replaying:',
                colour=discord.Colour.blue()
            )
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_client = ctx.message.guild.voice_client

            try:
                filename, title = await YTDLSources.from_url(self.history[0], loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename), after=lambda e: self.history[0])
                # voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                #                                      source=filename))
                embed.add_field(name="YouTube", value=title, inline=True)
                await ctx.send(embed=embed)
                pass
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description="Can't replay song"
                )
            return await ctx.send(embed=embed)

        @bot.command(name='back', help=helpMessages.BACK)
        async def back(ctx):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if len(self.history) == 0:
                    await ctx.send("**Can't go back, there is nothing left in the queue**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Going back a song...**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client

                    filename, title = await YTDLSources.from_url(self.history[0], loop=bot.loop)
                    voice_channel.play(
                        # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                     discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                      source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not go back in queue')
                return await ctx.send(embed=embed)

        @bot.command(name='history', help=helpMessages.HISTORY)
        async def history(ctx):
            embed = discord.Embed(
                title="History:",
                color=discord.Color.dark_grey()
            )
            connected = ctx.author.voice.channel

            if connected:
                if len(self.history) == 0:
                    await ctx.send("**Your history is currently empty**")
                else:
                    x = 0
                    while x < len(self.history):
                        filename, title = await YTDLSources.from_url(self.history[x], loop=bot.loop)
                        embed.add_field(name="Song " + str(x + 1), value=title, inline=True)
                        x += 1
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not view history'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='rewind', help=helpMessages.REWIND)
        async def rewind(ctx, num):
            embed = discord.Embed(
                title='Now Playing:',
                colour=discord.Colour.blue()
            )
            try:
                if len(self.history) == 0:
                    await ctx.send("**Can't rewind, there is nothing in your history**")
                else:
                    voice_client = ctx.message.guild.voice_client
                    if voice_client.is_playing():
                        voice_client.stop()
                    await ctx.send("**Rewinding**")
                    server = ctx.message.guild
                    voice_channel = server.voice_client
                    filename, title = await YTDLSources.from_url(self.history[int(num) - 1], loop=bot.loop)
                    voice_channel.play(
                    # discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                    discord.FFmpegPCMAudio(executable="/usr/local/Cellar/ffmpeg/4.3.2_4/bin/ffmpeg",
                                          source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
                    return
            except:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not rewind to specified song')
                return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MusicCommands(bot))
