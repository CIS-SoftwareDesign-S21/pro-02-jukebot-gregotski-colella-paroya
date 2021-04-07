import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from random import choice

load_dotenv()
TOKEN = open("token.txt", "r").read()
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
status = ['Taylor Swift','Harry Styles','Gucci Mane']


if __name__ == '__main__':

    for filename in os.listdir('./music_commands'):
        try:
            # bot.load_extension(f'music_commands.musicCommands')
            # bot.load_extension(f'music_commands.serverCommands')

            # loading the different commands but skips __init__ since it's just blank
            if filename != '__init__.py' and filename.endswith('.py'):
                bot.load_extension(f'music_commands.{filename[:-3]}')
        except Exception as error:
            print("Error: not able to load commands")
            print(error)
    print("Commands successfully loaded!")

@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))

@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot is online!")
    change_status.start()

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "general":
                await channel.send('Bot Activated..')
                await channel.send("jukebox.gif")
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}! Ready to jam out? See !help command for details!')




bot.run(TOKEN)
