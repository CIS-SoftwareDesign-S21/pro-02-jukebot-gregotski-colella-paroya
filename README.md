# JUKEBOT

# Vision
For Discord users who want to listen to music in a channel within a server with other Discord members so that everyone can synchronously listen to the same song. The JukeBot is a Discord music bot that the user can add to their channel to play music within the group chat that delivers excellent sound quality unlike playing music aloud in another open tab that relies on a user’s microphone. Our product enables Discord users to play from a variety of music services to share music in a group environment that creates a similar ambiance of playing music with a stereo in person, but in an online setting.

# Project Overview
Discord is a popular messaging platform where you can create servers and channels for people to join and message in. The concept of JukeBot allows you to be able to add the bot to your desired server and listen to music together in real time. JukeBot comes with a list of commands you can execute and it would be pulling music from YouTube which would then be streamed through a voice channel. 

For the completed project, using the bot would be integrated with the actual discord application. To use JukeBot, it would be added to the server as a bot and used through message commands. The commands would be done through the text chat using a special character such as ‘!’. For example, say I wanted to play a certain song, I would use the command “!play [song name].” The bot would then stream the song in the voice channel and to be able to listen to the song you would also have to be connected to that voice channel.

# Personas
### **Persona One:**

Matt, age 20, is a student at Temple University who lives on campus and has friends who attend the same college, but commute from home instead. They communicate with each other through Discord to collaborate on a group project for their marketing class in the Fox School of Business. The objective of this project is to create an advertisement for the new Temple footwear.

One of the requirements for the project is to decide which song to play in the background of the video for their advertisement. Since Matt and his friends are college students, they do not have as much money since they are currently unemployed, so they do not want to subscribe to Spotify music or any other music streaming service. They are interested in adding the JukeBot to their Discord channel to discuss which song, with YouTube as a source, to select for their project. They also find it convenient that this product states the artist and song without any confusion on what kind of version it is when searching it on their own.

### **Persona Two:**

Olivia is a college aged student, who is currently living at home because of the pandemic. With virtual classes, inability to meet in person, and other pandemic-related consequences, Olivia stays connected to her friends over Discord. They love listening to music together, but find it inconvenient when someone has to unmute themselves and listen to music from someone's microphone feed. Olivia struggles with this, in particular, because her friends can always hear her loud and chaotic family in the background. 

Olivia does not study anything tech related, but the commands will be simple enough that all she and her friends will need to worry about is what song they want to listen to! She is excited to use Jukebot so she can play music with her friends without them hearing her family, and so that each friend can control the music easily. 

### **Persona Three:**

Danny, age 22, is currently a gaming-streamer on Twitch living in Seattle, Washington. He has gained a significant following these past few months and uses Discord to keep his subscribers in the loop for when he's planning on streaming next. He enjoys holding monthly Discord nights with his friends and followers, where they can play games and listen to music together. 

For his next Discord night, Danny's been wanting to integrate a music bot for playing music in his server. He's excited to try out JukeBot, he has been looking for a reliable music bot for when they have listening parties or just streaming music in the background of their game nights. 

# Features & Commands
JukeBot allows for multiple users to interact with the bot at the same time and supports 
a multitude of different commands, such as maintaining a music queue and creating playlists.
Listed below are the different commands that are available for use:
- `!add:` adds a song to the queue.
- `!addto:` adds a song to a specific playlist
- `!back:` goes back a song in the queue and plays it.
- `!backfrom:` goes back to the previous song in a playlist.
- `!clear:` clears all the current songs in the queue.
- `!connect:` connects bot to the voice channel the user is in <p>
- `!create:` creates a new playlist.
- `!delete:`  deletes a specific playlist.
- `!disconnect:` disconnects bot from voice channel. <p>
- `!history:` shows the history of the queue.
- `!pause:` pauses the current audio playing from JukeBot.
- `!play [song name, link, title, keyword, etc.]:` plays the audio of the requested YouTube video<p><p>
- `!playfrom:` plays songs from a specific playlist
- `!playsongfrom:` plays specified song from specified playlist.
- `!remove:` removes a specific song from your queue.
- `!removefrom:` remove a song from a playlist.
- `!replay:` replays song that just ended.  
- `!resume:` resume the paused song or audio<p>
- `!rewind:` user can select a song that had already been played before to play again.
- `!shuffle:` plays a random song in the queue. 
- `!shufflefrom:` plays a random song in specified playlist.
- `!skip:` skips the current song in the queue and plays the next one.
- `!skipfrom:` skips the current song in the playlist and plays the next one.
- `!stop:` stops playing current song or audio<p>
- `!view:` view the current songs in the queue.
- `!viewplaylist:` view the current songs in a specific playlist.
- `!viewplaylists:` shows all created playlists
- `!volume:` changes the volume of the JukeBot.

# Trello Board
**[Link to Trello Board](https://trello.com/b/5LfhTkWk/jukebot)**

# How to Install
JukeBot is dependent on an OAuth2 token, so you would have to create your own
bot via [Discord's Developer Portal](https://discord.com/developers/docs/intro)
, and switch your token in. Also,
if hosting the bot, it is necessary to install any dependencies needed to run 
the bot, which are Python 3.9, discord.py, youtube_dl, and FFMPEG.
- Use the command `pip install discord.py` to install discord.py.
- Use the command `pip install youtube_dl` to install youtube_dl. 
- Download FFMPEG **[here](https://www.ffmpeg.org/)**

Before you start running your code, make sure to change 
  the executable path for FFMPEG in the code to match your own. 

Once these dependencies are installed and your FFMPEG path is changed, you
can run JukeBot through your chosen IDE or
command prompt!

If you are not hosting the bot, a user will only need to be in the discord server 
to utilize the JukeBot.

# Required Resources
- Python 3.9
- Discord Account
- [Discord's Python API](https://discordpy.readthedocs.io/en/latest/)
- [FFMPEG](https://www.ffmpeg.org/)
- [Discord Developer Portal Account](https://discord.com/developers/docs/intro)
