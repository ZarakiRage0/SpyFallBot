# SpyFallBot
A discord bot that plays SpyFall in a voice channel.

# About
SpyFallBot as the name suggests is a discord bot to play spayfall.  
Right now I'm kind of tinkering with discord api, and i thought why not make game bot.  
SpyFall was number one on my list since it's simple to configure and lots of fun to play.

# Before you run it
Before running the main script in bot.py, you would need to set up some variables :
- token : your discord token for the bot
- owner : Discord's api of the one managing the game ( showing list of players' cards, revaling the spy ...)

# Playing the game
First, the players would need to join a voice channel in a discord server.  
Also, you should have the bot in that server, otherwise it can't do much.  
Then type in a text channel ```spy start <name of the voice channel>```.  
The game ends after 10min and the bot sends a message to the channel annoucing its end.  
To reveal the spy, simply use ```spy reveal```.  
### Side Note
You can set up the game time through ```spy setTime <time in seconds>```.  
You can also set up custom locations with the ```spy add <location> <roles>``` command or you can just change up the json file if you wish to re-use your custom locations.

# Help 
For more info on what the commands do, use the ```spy help``` command.

Have fun with the bot. ^^

