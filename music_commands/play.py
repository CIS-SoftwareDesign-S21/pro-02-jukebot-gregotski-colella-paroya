import discord
import youtube_dl
from discord.ext import commands


class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command(name='play')
        async def play(msg, url):
            server = msg.message
            voice_client = bot.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url)
            #  players[server.id] = player
            player.start()


def setup(bot):
    bot.add_cog(play(bot))
