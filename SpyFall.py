import asyncio
from datetime import datetime

import discord
from discord.ext import commands


async def counter(ctx, game):
    await asyncio.sleep(game.gameTime)
    if game.gameIsLive:
        await ctx.send("Game has ended")


class SpyFall(commands.Cog):

    def __init__(self, bot, game, owner, embedColor, embedThumbnail):
        self.bot = bot
        self.game = game
        self.owner = owner
        self.embedColor = embedColor
        self.embedThumbnail = embedThumbnail

    async def sendEmbed(self, player):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Spy Fall"
        em.description = "Here is your card."
        em.colour = self.embedColor
        if player.role != "Spy":
            em.add_field(name="Location", value=self.game.location["title"])
        em.add_field(name="Role", value=player.role)
        await player.user.send(embed=em)

    async def sendRole(self, players):
        for player in players:
            await self.sendEmbed(player)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        commandlist = [e.name for e in self.bot.commands]
        em = discord.Embed()
        em.title = "Help"
        em.description = "Hey there, Hi there, Ho there!\n" \
                         "You can use me and my commands to play [spyfall](https://www.spyfall.app/) in discord.\n\n" \
                         "For details, use: ```spy help <command>```"
        em.set_thumbnail(url=self.embedThumbnail)
        em.colour = self.embedColor
        em.add_field(name="Commands", value="\n".join(commandlist))
        em.add_field(name="Usage", value="```spy help <command>```")

        await ctx.send(embed=em)

    @help.command()
    async def time(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - time"
        em.description = "Displays time elapsed since starting the game."
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy time```")
        await ctx.send(embed=em)

    @help.command()
    async def start(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - start"
        em.description = "Begins the SpyFall game.\n" \
                         "Sends to each player a card in DMs.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy start <voice_channel>```")
        em.add_field(name="Example", value="```spy start General```")

        await ctx.send(embed=em)

    @help.command()
    async def show(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - show"
        em.description = "Displays all the player's card.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy show```")

        await ctx.send(embed=em)

    @help.command()
    async def reference(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - reference"
        em.description = "Displays the list of locations.\n" \
                         "To be used by the spy.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy reference```")

        await ctx.send(embed=em)

    @help.command()
    async def add(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - add"
        em.description = "Adds a custom location.\n" \
                         "Must input a location and 7 roles.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy add <location> <role1>...<role7>```")

        await ctx.send(embed=em)

    @help.command()
    async def reveal(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - reveal"
        em.description = "Reveals the spy's card.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy reveal```")

        await ctx.send(embed=em)

    @help.command()
    async def rules(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - rules"
        em.description = "Explains the rules of SpyFall.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy rules```")

        await ctx.send(embed=em)

    @help.command()
    async def flush(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - flush"
        em.description = "Clear the locations\n" \
                         "To be used when you want to play with custom only."
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy flush```")

        await ctx.send(embed=em)

    @help.command()
    async def setTime(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "Help - setTime"
        em.description = "Sets the time limit for one game.\n"
        em.colour = self.embedColor
        em.add_field(name="Usage", value="```spy setTime```")

        await ctx.send(embed=em)

    @commands.command()
    async def rules(self, ctx):
        em = discord.Embed()
        em.set_thumbnail(url=self.embedThumbnail)
        em.title = "SpyFall"
        em.description = "How to play\n"
        em.colour = self.embedColor
        em.add_field(name="Rules", value="Each player will get assigned a role and a location.\n"
                                         "Every player's location is  the same but the roles are different.\n"
                                         "One player is chosen to be the spy.\n"
                                         "The spy doesn't know the location nor the roles of the group.\n"
                                         "His job to find out the location.\n"
                                         "If the spy guesses the location the spy wins.\n"
                                         "If the group guesses who the spy is the group wins.\n"
                                         "You achieve this by taking turns asking questions to one another that "
                                         "you might think would be revealing about who the spy is,"
                                         " or in the spy's case where the group is located.")
        await ctx.send(embed=em)

    @commands.command()
    async def start(self, ctx, arg):
        voicechannel = str(arg)
        for channel in ctx.guild.voice_channels:
            if channel.name == voicechannel:
                if len(channel.members) > self.game.maxPlayers:
                    await ctx.send("Party is way too big")
                elif len(channel.members) == 0:
                    await ctx.send("Party is empty")
                else:
                    length = len(channel.members)
                    await ctx.send("Starting game : " + str(length) + " out of 8 players")
                    self.game.play(channel.members)
                    await self.sendRole(self.game.players)
                    self.bot.loop.create_task(counter(ctx, self.game))
                return
        await ctx.send("I doubt the channel you've just send is valid")

    @commands.command()
    async def show(self, ctx):
        if str(ctx.author) == self.owner:
            for player in self.game.players:
                user = player.user
                em = discord.Embed()
                em.set_thumbnail(url=user.avatar_url)
                em.title = "Spy Fall"
                em.description = "Player : " + user.name
                em.colour = self.embedColor
                if player.role != "spy":
                    em.add_field(name="Location", value=self.game.location["title"])
                em.add_field(name="Role", value=player.role)
                await ctx.send(embed=em)
        else:
            await ctx.send("You're not the boss of me")

    @commands.command()
    async def reveal(self, ctx):
        if str(ctx.author) == self.owner:
            if self.game.get_spy() is not None:
                spy = self.game.get_spy().user
                em = discord.Embed()
                em.set_thumbnail(url=spy.avatar_url)
                em.title = "Spy Fall"
                em.colour = self.embedColor
                em.add_field(name="Spy", value=spy.name)
                await ctx.send(embed=em)
                self.game.gameEnd()
            else:
                await ctx.send("game hasn't started yet.")
        else:
            await ctx.send("You're not the boss of me")

    @commands.command()
    async def time(self, ctx):
        if self.game.startTime is None:
            await ctx.send("Game hasn't started yet")
        else:
            playTime = datetime.now() - self.game.startTime
            await ctx.send("time elapsed since game has started : " + str(playTime))

    @commands.command()
    async def reference(self, ctx):
        em = discord.Embed()
        em.title = "Spy Fall"
        em.description = "Here is your reference."
        em.colour = self.embedColor
        separator = "\n"
        locations = [e["title"] for e in self.game.data]
        em.add_field(name="Locations", value=separator.join(locations))
        await ctx.send(embed=em)

    @commands.command(name="add")
    async def add(self, ctx, *args):
        if len(args) != 8:
            await ctx.send("I doubt it's a location, agent.")
        else:
            location = {"title": str(args[0]), "roles": list(args[1:])}
            self.game.add_location(location)

    @commands.command(name="flush")
    async def flush(self, ctx):
        self.game.data = {}
        await ctx.send("flushed.")

    @commands.command(name="setTime")
    async def setTime(self, ctx, arg):
        gameTime = int(str(arg))
        self.game.set_gameTime(gameTime=gameTime)
        await ctx.send("Time is set.")
