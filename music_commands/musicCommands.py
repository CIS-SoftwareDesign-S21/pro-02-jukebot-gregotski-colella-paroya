import asyncio
import functools

import discord
from discord.ext import commands, tasks
import os

from discord.utils import get
from dotenv import load_dotenv
import youtube_dl
from collections import deque
import helperFunctions
import helpMessages
import asyncio
from asyncio import run_coroutine_threadsafe as rct

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


class YTDLError(Exception):
    pass

class YTDLSources(discord.PCMVolumeTransformer, commands.Cog):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
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
        #self.play_next_song = asyncio.Event()



        async def play_next(ctx):
            if len(self.queue) >= 1:
                del self.queue[0]
                vc = get(self.bot.voice_clients, guild=ctx.guild)

                filename = await YTDLSources.from_url(self.queue[0], loop=bot.loop)
                vc.play(discord.FFmpegPCMAudio(source=filename), after=lambda e: play_next(ctx))
                asyncio.run_coroutine_threadsafe(await ctx.send("No more songs in queue."),loop=asyncio.get_event_loop())


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
                        voice_channel.play(discord.FFmpegPCMAudio(source=filename), after=lambda e:
                        play_next(ctx))

                            #voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe",
                                #                                  source=filename))
                    embed.add_field(name="YouTube", value=title, inline=True)
                    await ctx.send(embed=embed)
                    del (self.queue[0])
                    pass


                except:
                    # await ctx.send("**Can't play song**")
                    embed = discord.Embed(
                        title='Error!',
                        colour=discord.Colour.red(),
                        description='Cannot play song'
                    )
                    return await ctx.send(embed=embed)

        @bot.command(name='rewind', help=helpMessages.VIEW)
        async def rewind(ctx, url):

            if url is not None:
                # if argument not a youtube link, convert
                if not ("watch?v=" in url):
                    url = helperFunctions.convert_to_link(url)
                    # if converting to youtube link was unsuccessful
                    if not ("watch?v=" in url):
                        await ctx.send("Can't find result from Youtube")
                        return

            try:

                server = ctx.message.guild
                voice_channel = server.voice_client
                f = await YTDLSources.from_url(url, loop=bot.loop)
           #     f2 = f.seek(0)
                voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f.seek(0)))
                await ctx.send("Rewinding song...")
            except:
                await ctx.send("Cannot rewind song")


        @bot.command(name='replay')
        async def replay(ctx):
            voice_client = ctx.message.guild.voice_client
            if not voice_client.is_playing():
                return await ctx.send('Nothing being played at the moment.')
          #  try:

        #        server = ctx.message.guild
        #        voice_channel = server.voice_client
        #        filename = await YTDLSources.from_url(self.history[0], loop=bot.loop)
        #        voice_channel.play(filename, after=lambda e: self.history[0].duration()) #print('Player error: %s' % e) if e else None)
                #voice_channel.play(
                #    discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
           # voice_channel.play(FFmpegPCMAudio(audio), after=lambda e: )
          #  if ctx.voice_client.loop:
        #        await ctx.message.add_reaction('✅')
         #   except:
         #       await ctx.send("Can't replay song")

     #   @bot.command(name='seek', help=helpMessages.VIEW)
      #  async def seek(ctx,num):

         #   fileOpen = open(file)
         #   f = fileOpen.seek(int(num))
        #    server = ctx.message.guild
          #  voice_channel = server.voice_client
          #  voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f))

        @bot.command(name='view', help=helpMessages.VIEW)
        async def view(ctx):

            embed = discord.Embed(
                title="Queue:",
                color=discord.Color.purple()
            )
            connected = ctx.author.voice.channel
            #x = 0
            if connected:
                if len(self.queue) == 0:
                    await ctx.send("**Your queue is currently empty**")
                else:
                    x = 0
                    while x < len(self.queue):
                        filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
                        embed.add_field(name="Song " + str(x + 1), value=title, inline=True)
                        #filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
                        #embed.add_field(name="Track", value=title, inline=True)
                        x += 1
                    await ctx.send(embed=embed)
                    return
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not view queue'
                )
                return await ctx.send(embed=embed)
           # try:
           #     if len(self.queue) == 0:
           #         await ctx.send("Your queue is currently empty")
           #     else:
           #         while x <= len(self.queue):
           #             filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
           #             #embed.add_field(name="Song " + str(x + 1), value=title, inline=True)
           #            # filename, title = await YTDLSources.from_url(self.queue[x], loop=bot.loop)
           #             embed.add_field(name="Track", value=title, inline=True)
           #             x += 1
           #         await ctx.send(embed=embed)
           # except:

                #embed = discord.Embed(
                #    title='Error!',
                #    colour=discord.Colour.red(),
                #    description='Could not view queue'
                #)
                #return await ctx.send(embed=embed)

        @bot.command(name='remove', help=helpMessages.REMOVE)
        async def remove(ctx, number):
            try:
                if len(self.queue) != 0:
                    del (self.queue[int(number)])
                    await ctx.send("**Song was deleted from queue**")
                else:
                    await ctx.send("**Queue is currently empty**")
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
                await ctx.send("**Song added to queue**")
                return
            else:
                embed = discord.Embed(
                    title='Error!',
                    colour=discord.Colour.red(),
                    description='Could not add song to queue'
                )
                return await ctx.send(embed=embed)

        @bot.command(name='viewplaylists', help=helpMessages.VIEW_PLAYLISTS)
        async def viewplaylists(ctx):

            embed = discord.Embed(
                title="Playlists:",
                color=discord.Color.purple()
            )
            x = 0
            try:
                if len(self.totalPlaylists) == 0:
                    await ctx.send("**There are no playlists created**")
                else:
                    while x <= len(self.playlists):
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
            if connected:
                try:
                    if self.totalPlaylists.__contains__(playlist):
                        num = self.totalPlaylists.index(playlist)
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
                            x = 0
                            filename, title = await YTDLSources.from_url(self.playlists[num][0], loop=bot.loop)
                            voice_channel.play(
                                discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=filename))
                            #  x += 1
                            embed.add_field(name="YouTube", value=title, inline=True)
                            await ctx.send(embed=embed)
                            pass

                            await ctx.send('**Now playing:** {}'.format(title))

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
                color=discord.Color.dark_teal()
            )

            x = 0
            try:
                if self.totalPlaylists.__contains__(playlist):
                    num = self.totalPlaylists.index(playlist)
                    if len(self.playlists[num]) == 0:
                        await ctx.send("**Your playlist is currently empty**")
                    else:
                        while x <= len(self.playlists[num]):
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
                        description='That is louder than the music goes! Please enter a number between 1-100'
                    )
                    return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MusicCommands(bot))

