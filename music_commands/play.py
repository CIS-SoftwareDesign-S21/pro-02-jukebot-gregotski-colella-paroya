import discord
from discord.ext import commands

import YTDLSource


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='play')
        async def play(ctx, url):
            try:
                server = ctx.message.guild
                voice_channel = server.voice_client
                async with ctx.typing():
                    filename = await YTDLSource.from_url(url, loop=bot.loop)
                    voice_channel.play(discord.FFmpegPCMAudio(executable="FFMPEG.exe", source=filename))
                await ctx.send('**Now playing:** {}'.format(filename))
            except:
                await ctx.send("The bot is not connected to a voice channel.")


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


def setup(bot):
    bot.add_cog(play(bot))
