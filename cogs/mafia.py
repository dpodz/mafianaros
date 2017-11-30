import discord
import asyncio
from discord.ext import commands
from random import randint

client = discord.Client()

class Mafia:
    """Mafianaros bot for playing mafia!"""

    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.mafiaroles = []
        self.civroles = []
        self.mafiadict = {}
        self.civdict = {}

    @commands.command()
    async def mafiareset(self):
        """Initializes a game of mafia!"""
        
        await self.bot.say("Initializing a mafia game!")
        self.players = []
        self.mafiaroles = []
        self.civroles = []
        self.mafiadict = {}
        self.civdict = {}
        await self.bot.say( 'To do:\n' +
                            'Add players with !addplayer "name"\n' +
                            'Add mafia roles with !addmafia "rolename"\n' +
                            'Add civilian roles with !addciv "rolename"\n' +
                            'Start the game with !mafiastart')
        
        
    @commands.command()
    async def addplayer(self, user : discord.Member):
        """Add a player to the current game"""
        self.players.append(user)
        await self.bot.say(user.mention + ' added!')
        
    @commands.command()
    async def mafiaplayers(self):
        """Lists players in current game"""
        playerlist = 'Players:\n'
        for player in self.players:
            playerlist += player.mention + '\n'
        await self.bot.say(playerlist)
        
    @commands.command()
    async def addmafia(self, rolename):
        """Add a mafia role"""
        self.mafiaroles.append(rolename)
        self.mafiadict[rolename] = []
        await self.bot.say(rolename + ' added to mafia roles')
        
    @commands.command()
    async def addciv(self, rolename):
        """Add a civilian role"""
        self.civroles.append(rolename)
        self.civdict[rolename] = []
        await self.bot.say(rolename + ' added to civ roles')
    
    @commands.command()
    async def mafiastart(self):
        """Generates roles for players and sends pms"""
        tempPlayersList = list(self.players)
        # Generate civilian roles
        await self.bot.say('Generating civ roles...')
        for civrole in self.civroles:
            #await self.bot.say('len(tempPlayersList) = ' + str(len(tempPlayersList)))
            randPlayer = randPlayer = 0 if len(tempPlayersList) == 1 else randint(0, len(tempPlayersList)-1)
            self.civdict[civrole].append(tempPlayersList[randPlayer])
            tempPlayersList.pop(randPlayer)
        # Generate mafia roles
        await self.bot.say('Generating mafia roles...')
        for mafiarole in self.mafiaroles:
            #await self.bot.say('len(tempPlayersList) = ' + str(len(tempPlayersList)))
            randPlayer = 0 if len(tempPlayersList) == 1 else randint(0, len(tempPlayersList)-1)
            self.mafiadict[mafiarole].append(tempPlayersList[randPlayer])
            tempPlayersList.pop(randPlayer)
        # Fill in rest of players as generic civilians
        await self.bot.say('Setting remaining players as civilians...')
        self.civdict['civilian'] = []
        for player in tempPlayersList:
            self.civdict['civilian'].append(player)
        await self.bot.say('Aaaaand sending out messages!')
        for mafiaRole, mafiaUsers in self.mafiadict.items():
            # Make a string of all mafiaUsers
            mafiaUsersString = ""
            for mafiaUser in mafiaUsers:
                mafiaUsersString += mafiaUser.mention + " "
            for mafiaUser in mafiaUsers:
                await self.bot.say(mafiaUser.mention)
                await self.bot.send_message(mafiaUser,  'Your role is: ' + mafiaRole + '\n'
                                                        'Your fellow mafiosos are ' + mafiaUsersString)
        for civRole, civUsers in self.civdict.items():
            for civUser in civUsers:
                await self.bot.say(civUser.mention)
                await self.bot.send_message(civUser, 'Your role is: ' + civRole)
        
            

def setup(bot):
    bot.add_cog(Mafia(bot))
