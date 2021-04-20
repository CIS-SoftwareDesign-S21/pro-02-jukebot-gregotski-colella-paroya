import discord
from discord.ext import commands


class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.group(invoke_without_command=True)
        async def help(ctx):
            em = discord.Embed(title="Help",
                               description="Use !help [command name] for extended information about the command!",
                               colour=discord.Colour.dark_gold())

            em.add_field(name='Music Commands', value="•add\n"
                                                      "•addto\n"
                                                      "•back\n"
                                                      "•backfrom\n"
                                                      "•clear\n"
                                                      "•create\n"
                                                      "•delete\n"
                                                      "•history\n"
                                                      "•pause\n"
                                                      "•play\n"
                                                      "•playfrom\n"
                                                      "•playsongfrom\n"
                                                      "•remove\n"
                                                      "•removefrom\n"
                                                      "•replay\n"
                                                      "•resume\n"
                                                      "•rewind\n"
                                                      "•seek\n"
                                                      "•shuffle\n"
                                                      "•shufflefrom\n"
                                                      "•skip\n"
                                                      "•skipfrom\n"
                                                      "•stop\n"
                                                      "•view\n"
                                                      "•viewplaylist\n"
                                                      "•viewplaylists\n"
                                                      "•volume")
            em.add_field(name="Server Commands", value="•connect\n"
                                                       "•disconnect")
            em.add_field(name="Misc.", value="helloworld")

            await ctx.send(embed=em)

        @help.command()
        async def add(ctx):
            em = discord.Embed(title="Add", description="Adds a song to the queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!add ['song name', url/youtube link, 'keywords', etc.]")
            await ctx.send(embed=em)

        @help.command()
        async def addto(ctx):
            em = discord.Embed(title="Addto", description="Add a song to a specific playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:",
                         value="!addto [playlist name]['song name', url/youtube link, 'keywords', etc.]")
            em.add_field(name="Example", value="!addto test 'taylor swift'")
            await ctx.send(embed=em)

        @help.command()
        async def back(ctx):
            em = discord.Embed(title="Back", description="Goes back a song in the queue and plays it.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!back")
            await ctx.send(embed=em)

        @help.command()
        async def backfrom(ctx):
            em = discord.Embed(title="Backfrom", description="Goes back to the previous song in a playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!backfrom")
            await ctx.send(embed=em)

        @help.command()
        async def clear(ctx):
            em = discord.Embed(title="Clear", description="Clears all the current songs in the queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!clear")
            await ctx.send(embed=em)

        @help.command()
        async def create(ctx):
            em = discord.Embed(title="Create", description="Creates a new playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!create [playlist name]")
            await ctx.send(embed=em)

        @help.command()
        async def delete(ctx):
            em = discord.Embed(title="Delete", description="Deletes a playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!delete [playlist name]")
            await ctx.send(embed=em)

        @help.command()
        async def history(ctx):
            em = discord.Embed(title="History", description="Shows the history of the queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!history")
            await ctx.send(embed=em)

        @help.command()
        async def pause(ctx):
            em = discord.Embed(title="Pause", description="Pauses the current audio playing from JukeBot.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!pause")
            await ctx.send(embed=em)

        @help.command()
        async def play(ctx):
            em = discord.Embed(title="Play",
                               description="When !play is followed by no arguments, audio will play from the top of "
                                           "the queue. When" \
                                           "followed by a link, audio will play from the designated Youtube video. "
                                           "Finally, when followed" \
                                           "by text, the audio of the first Youtube search result will play. If the "
                                           "search is longer than one" \
                                           "word, make sure to put text in quotation marks.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value='!play\n!play [url]\n!play "Harry Styles Golden"')
            await ctx.send(embed=em)

        @help.command()
        async def playfrom(ctx):
            em = discord.Embed(title="Playfrom", description="Plays songs from a specific playlist",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!playfrom [playlist name]")
            await ctx.send(embed=em)

        @help.command()
        async def playsongfrom(ctx):
            em = discord.Embed(title="Playsongfrom", description="Plays specified song from specified playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!playsongfrom [playlist name] [song number]")
            await ctx.send(embed=em)

        @help.command()
        async def remove(ctx):
            em = discord.Embed(title="Remove", description="Removes a specific song from your queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!remove [song number]")
            await ctx.send(embed=em)

        @help.command()
        async def removefrom(ctx):
            em = discord.Embed(title="Removefrom", description="Remove a song from a playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!removefrom [playlist name] [song number]")
            await ctx.send(embed=em)

        @help.command()
        async def replay(ctx):
            em = discord.Embed(title="Replay", description="Replays song that just ended.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!replay")
            await ctx.send(embed=em)

        @help.command()
        async def resume(ctx):
            em = discord.Embed(title="Resume", description="Resumes song that was paused.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!resume")
            await ctx.send(embed=em)

        @help.command()
        async def rewind(ctx):
            em = discord.Embed(title="Replay",
                               description="User can select a song that had already been played before to play again.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!rewind [song number]")
            await ctx.send(embed=em)

        @help.command()
        async def seek(ctx):
            em = discord.Embed(title="Seek",
                               description="Lets the user change the timestamp of the song that is currently playing.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!seek 1:30")
            await ctx.send(embed=em)

        @help.command()
        async def shuffle(ctx):
            em = discord.Embed(title="Shuffle",
                               description="Plays a random song in the queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!shuffle")
            await ctx.send(embed=em)

        @help.command()
        async def shufflefrom(ctx):
            em = discord.Embed(title="ShuffleFrom",
                               description="Plays a random song in specified playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!shufflefrom [playlist name]")
            await ctx.send(embed=em)

        @help.command()
        async def skip(ctx):
            em = discord.Embed(title="Skip",
                               description="Skips the current song in the queue and plays the next one.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!skip")
            await ctx.send(embed=em)

        @help.command()
        async def skipfrom(ctx):
            em = discord.Embed(title="SkipFrom",
                               description="Skips the current song in the playlist and plays the next one.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!skipfrom")
            await ctx.send(embed=em)

        @help.command()
        async def stop(ctx):
            em = discord.Embed(title="Stop",
                               description="Stops the current audio playing, and clears the song. You cannot resume"
                                           "song after stopping.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!stop")
            await ctx.send(embed=em)

        @help.command()
        async def view(ctx):
            em = discord.Embed(title="View",
                               description="View the current songs in the queue.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!view")
            await ctx.send(embed=em)

        @help.command()
        async def viewplaylist(ctx):
            em = discord.Embed(title="ViewPlaylist",
                               description="View the current songs in a specific playlist.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!viewplaylist [playlist name]")
            await ctx.send(embed=em)

        @help.command()
        async def viewplaylists(ctx):
            em = discord.Embed(title="ViewPlaylists",
                               description="Show all created playlists.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!viewplaylists")
            await ctx.send(embed=em)

        @help.command()
        async def volume(ctx):
            em = discord.Embed(title="Volume",
                               description="Change the volume of the JukeBot.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!volume [volume number]")
            await ctx.send(embed=em)

        @help.command()
        async def connect(ctx):
            em = discord.Embed(title="Connect",
                               description="Connects JukeBot to your voice channel that you're in.",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!connect")
            await ctx.send(embed=em)

        @help.command()
        async def disconnect(ctx):
            em = discord.Embed(title="Disconnect",
                               description="Disconnects JukeBot from voice channel",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!disconnect")
            await ctx.send(embed=em)

        @help.command()
        async def helloworld(ctx):
            em = discord.Embed(title="Hello World",
                               description="Basic hello work implementation, when command is used the JukeBot "
                                           "responds with its own 'Hello World!'",
                               colour=discord.Colour.dark_orange())
            em.add_field(name="Syntax:", value="!helloworld")
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(helpCommand(bot))
