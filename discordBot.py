import discord
from discord.ext import commands
from game import Game
from SpyFall import SpyFall


def setup_cog(bot):
    thumbnail = "https://i.imgur.com/oF7C1wp.png"
    color = 2507490
    game = Game("spyfall.json")
    owner = "<The owner's discord ID>"
    cog = SpyFall(bot=bot, game=game, owner=owner, embedColor=color, embedThumbnail=thumbnail)
    bot.add_cog(cog)


def setup_bot():
    prefix = 'spy '
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    bot.remove_command("help")
    return bot


def run(bot, token):
    bot.run(token)


if __name__ == '__main__':
    token = "<your discord token>"
    bot = setup_bot()
    setup_cog(bot)
    print([command.name for command in bot.commands])
    bot.run(token)