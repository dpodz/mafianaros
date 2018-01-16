import discord
import asyncio
import random
from enum import Enum
from discord.ext import commands

#?client = discord.Client()

# Settings
MESSAGE_NON_ERRORS = False

# Enumerations
# Supported mafia roles
class MafiaRoles(Enum):
    Godfather = 'Godfather'
    Henchman = 'Henchman'
    
# Supported civ roles
class CivRoles(Enum):
    Civilian = 'Civilian'
    Doctor = 'Doctor'
    Detective = 'Detective'

# Role commands
class RoleCommands(Enum):
    Setup = '!addplayer "user"\n!addmafia "mafiarole"\n!addciv "civrole"\n!setlynchmode "lynchmode"\n!mafiastart\n'
    All = '!lynch "user"\n!lynch "" (sets to no lynch)\n!lynchlist\n'
    Mafia = '!mafiamsg "message"\n"'
    Godfather = '!mafiakill "user"\n' 
    Henchman = 'Henchman have no special commands. You suck\n'
    Civilian = 'Civilians have no special commands. You suck\n'
    Doctor = '!doctorsave "user"\n'
    Detective = '!detectivefind "user"\n'
# Possible game states
class GameStates(Enum):
    LOADING = 0
    DAY     = 1
    NIGHT   = 2
    END     = 9
    
# Possible lynch modes
class LynchModes(Enum):
    PLURALITY = 0
    MAJORITY  = 1
    
# Messages
ROLE_ERR_MSG = "Role add failed. Make sure first letter is capitalized."

class MafiaPlayer:
    """this class stores all the mafia player data"""
    def __init__(self, user : discord.Member):
        self.user = user
        self.lynchchoice = None # lynchchoice is a discord.Member
        self.role = ''
        self.team = ''
        self.isAlive = True
        self.causeOfDeath = ''

    def setrole(self, rolename):
        self.role = rolename
        
    def setteam(self, teamname):
        self.team = teamname
    
class Mafia:
    """Mafianaros cog for playing mafia!"""

    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.mafiaroles = []
        self.civroles = []
        self.gamestate = GameStates.LOADING
        self.lynchmode = LynchModes.MAJORITY
        self.day = 0
         
    @commands.command(pass_context=True)
    async def mafiahelp(self, ctx):
        mafiahelpstring = "These are the mafia commands available to you:\n```"
        if (self.gamestate == GameStates.LOADING):
            mafiahelpstring += RoleCommands.Setup.value
        else:
            mafiahelpstring += RoleCommands.All.value
            # find the player by id
            for player in self.players:
                if (player.user.id == ctx.message.author.id):
                    if (player.team == 'Mafia'):
                        mafiahelpstring += RoleCommands.Mafia.value
                    if (player.role in MafiaRoles.__members__ or player.role in CivRoles.__members__):
                        mafiahelpstring += RoleCommands[player.role].value
                    break
        # send the help string
        mafiahelpstring += "```"
        await self.bot.send_message(ctx.message.author, mafiahelpstring)
    
    @commands.command()
    async def mafiareset(self):
        """Initializes a game of mafia!"""
        
        await self.bot.say('Initializing a mafia game!')
        self.players = []
        self.mafiaroles = []
        self.civroles = []
        self.gamestate = GameStates.LOADING
        self.day = 0
        
        await self.bot.say( 'To do:\n' +
                            'Add players with !addplayer "name"\n' +
                            'Add mafia roles with !addmafia "rolename"\n' +
                            'Add civilian roles with !addciv "rolename"\n' +
                            'Start the game with !mafiastart')
        
        
    @commands.command()
    async def mafiastatus(self):
        """Displays gamestate, including players, mafia roles, civ roles, day, etc"""
        # list players
        playerlist = 'Players:\n'
        for mafiaplayer in self.players:
            if (mafiaplayer.isAlive):
                playerlist += mafiaplayer.user.name + '\n'
            else:
                playerlist +=   ('~~' + mafiaplayer.user.name + 
                                ' the ' + mafiaplayer.role + ', ' +
                                mafiaplayer.causeOfDeath + '~~\n')
        await self.bot.say(playerlist)
        # list mafia roles
        await self.bot.say("Mafia roles: " + ", ".join(self.mafiaroles))
        # list civ roles
        await self.bot.say("Civ (special) roles: " + ", ".join(self.civroles))
        # Say which day it is
        await self.bot.say("Day: " + str(self.day))
        # Say gamestate
        await self.bot.say("Gamestate: " + self.gamestate.name)
        # Say lynchmode
        await self.bot.say("Lynch Mode: " + self.lynchmode.name)
            
    
    @commands.command()
    async def lynchlist(self):
        """Lists the lynch choices of the players in the game"""
        lynchdict = {}
        lynchdict['Nolynch'] = list()
        #do a pass to contruct the lynch dictionary
        for player in self.players:
            if (player.isAlive):
                lynchdict[player.user.name] = list()
                
        #do a pass to contruct the lynch lists
        for player in self.players:
            if (player.isAlive):
                if player.lynchchoice == None:
                    lynchdict['Nolynch'].append(player.user.name)
                else: 
                    lynchdict[player.lynchchoice.name].append(player.user.name)
        
        #do a pass to print the lynch dict
        lynchliststring = ""
        for playername, lynchlist in lynchdict.items():
            lynchliststring += playername + ": (" + str(len(lynchlist)) + ") " + ', '.join(lynchlist) + "\n"
        await self.bot.say(lynchliststring)
        
    @commands.command()
    async def addplayer(self, user : discord.Member):
        """Add a player to the current game"""
        if (self.gamestate != GameStates.LOADING):
            await self.bot.say('Not currently in loading state')
            return
        mafiaplayer = MafiaPlayer(user)
        self.players.append(mafiaplayer)
        if (MESSAGE_NON_ERRORS): 
            await self.bot.say(user.mention + ' added!')
        
    @commands.command()
    async def addmafia(self, rolename):
        """Add a mafia role"""
        if (self.gamestate != GameStates.LOADING):
            await self.bot.say('Not currently in loading state')
            return
        if (rolename in MafiaRoles.__members__):
            self.mafiaroles.append(rolename)
            if (MESSAGE_NON_ERRORS):
                await self.bot.say(rolename + ' added to mafia roles')
        else: 
            await self.bot.say(ROLE_ERR_MSG)
        
    @commands.command()
    async def addciv(self, rolename):
        """Add a civilian role"""
        if (self.gamestate != GameStates.LOADING):
            await self.bot.say('Not currently in loading state')
            return
        if (rolename in CivRoles.__members__):
            self.civroles.append(rolename)
            if (MESSAGE_NON_ERRORS):
                await self.bot.say(rolename + ' added to civ roles')
        else: 
            await self.bot.say(ROLE_ERR_MSG)
    
    @commands.command()
    async def savegame(self):
        """Saves the current gamestate"""
        await self.bot.say('Save feature not yet implemented')
        
    @commands.command()
    async def setlynchmode (self, lynchmode):
        """sets the lynch mode. Type !setlynchmode list to list acceptable modes"""
        if (lynchmode == 'MAJORITY'):
            self.lynchmode = LynchModes.REQUIREMAJORITY
            await self.bot.say("Lynch Mode set to require majority of players to vote on the same player")
        elif (lynchmode == 'PLURALITY'):
            self.lynchmode = LynchModes.LYNCHMOST
            await self.bot.say("Lynch Mode set to lynch the player with the highest number of votes")
        else:
            await self.bot.say("That is not an acceptable lynch mode")
            await self.bot.say("Available lynchmodes are: " + ", ".join(list(map(str, LynchModes))))
    
    @commands.command()
    async def mafiastart(self):
        """Generates roles for players and sends pms"""
        playersRefList = list(range(0,len(self.players)))
        # Generate civilian roles
        await self.bot.say('Generating civ roles...')
        for civrole in self.civroles:
            randPlayer = random.choice(playersRefList)
            self.players[randPlayer].role = civrole
            self.players[randPlayer].team = 'Civilian'
            playersRefList.remove(randPlayer)
        
        # Generate mafia roles
        await self.bot.say('Generating mafia roles...')
        for mafiarole in self.mafiaroles:
            randPlayer = random.choice(playersRefList)
            self.players[randPlayer].role = mafiarole
            self.players[randPlayer].team = 'Mafia'
            playersRefList.remove(randPlayer)
        
        # Fill in rest of players as generic civilians
        await self.bot.say('Setting remaining players as civilians...')
        for playerRef in playersRefList:
            self.players[playerRef].role = CivRoles.Civilian.value
            self.players[playerRef].team = 'Civilian'
        await self.bot.say("Lynching Malc...")
        await self.bot.say('Aaaaand sending out messages!')
        # Generate a string of all the mafiosos
        mafiaPlayersString = ""
        for player in self.players: 
            # Make a string of all mafiaUsers
            if player.team == 'Mafia':
                mafiaPlayersString += player.user.name + ", "
                
        # Send out messages to all players
        for player in self.players:
            await self.bot.send_message(player.user, "Your role is: " + player.role)
            if player.team == 'Mafia':
                await self.bot.send_message(player.user, 'Your fellow mafiosos are ' + mafiaPlayersString)
        
        await self.daystart()
    
    # !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Commands while game is running
    # !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @commands.command(pass_context=True)
    async def lynch(self, ctx, user : discord.Member = None):
        """set which user you'd like to lynch. Type just '!lynch' to nolynch"""
        if (self.gamestate != GameStates.DAY):
            await self.bot.say("It's not lynching time right now")
            return
        elif (user == None):
            for player in self.players:
                if (player.user.id == ctx.message.author.id):
                    player.lynchchoice = None
                    return
        elif (not (await self.userisalive(user)) ):
            await self.bot.say("That user is not in this game or is already dead")
            return
        elif (not (await self.userisalive(ctx.message.author)) ):
            await self.bot.say("You're dead, you're not allowed to vote (or you're not in the game)")
            return
        else:
            for player in self.players:
                if (player.user.id == ctx.message.author.id):
                    player.lynchchoice = user
                    break
            return
            
    @commands.command()
    async def dayend(self):
        """end the current day, count lynch votes, etc"""
        if (self.gamestate != GameStates.DAY):
            await self.bot.say("It's not daytime right now, silly")
        elif (await self.checkconditions()):
            pass
        else:
            #count lynch votes
            if(not (await self.commitlynch()) ):
                return
            # reset the lynch list, since it's used by the special roles
            for player in self.players:
                player.lynchchoice = None
            await self.bot.say('The day has ended and lynching is complete. Night has fallen upon us. The mafia and special civs may message me with their commands')
            self.gamestate = GameStates.NIGHT
            
    
    @commands.command()
    async def nightend(self):
        """end the current night, resolve nighttime activities like mafia murder and whatnot"""
        if (self.gamestate != GameStates.NIGHT):
            await self.bot.say("It's not nighttime right now, silly")
        # Construct the doctor save list (of user id's)
        savelist = list()
        for player in self.players:
            if (player.role == 'Doctor' and player.lynchchoice != None and player.isAlive):
                savelist.append(player.lynchchoice.id)
        
        # Conduct nightly murders by mafia
        # Tell the sleuths what roles their targets are
        for player in self.players:
            if (not player.isAlive):
                pass
            elif (player.role == 'Godfather'):
                if (player.lynchchoice == None):
                    await self.bot.say("The mafia didn't try to murder anyone???")
                elif (player.lynchchoice.id in savelist):
                    await self.bot.say("The mafia tried to murder " + player.lynchchoice.mention + " but the doctor managed to save them in time!")
                else:
                    # find the player who's going to be killed
                    for murdered in self.players:
                        if (murdered.user.id == player.lynchchoice.id):
                            murdered.isAlive = False
                            murdered.causeOfDeath = "murdered by the mafia"
                    await self.bot.say("The mafia has successfully murdered " + player.lynchchoice.mention)
            elif (player.role == 'Detective'):
                if (player.lynchchoice == None):
                    await self.bot.send_message(player.user, "You didn't try to detect anyone tonight? What are you doing...")
                else:
                    detectrole = await getuserrole(player.lynchchoice)
                    detectteam = await getuserrole(player.lynchchoice)
                    await self.bot.send_message(player.user, "You have managed to discover that " + player.lynchchoice.mention + " works for team " + detectteam + " and is the " + detectrole)
        
        await self.daystart()
    
    # !~~~~~~~~~~~~~~~~~~~~
    # Special Role Commands
    # !~~~~~~~~~~~~~~~~~~~~
    
    @commands.command(pass_context=True)
    async def mafiamsg(self, ctx, msg : str = ""):
        """ Allows the mafia to message one another. Automatically sends your message to the rest of the mafia members"""
        message = ctx.message.author.name + " says: " + msg
        for player in self.players:
            if (player.team == 'Mafia' and player.user.id != ctx.message.author.id):
                await self.bot.send_message(player.user, message)
                
    
    @commands.command(pass_context=True)
    async def mafiakill(self, ctx, user : discord.Member = None):
        """ Allows the mafia to set who they want to kill. Usable only by the Godfather role"""
        role = await self.getuserrole(ctx.message.author)
        if (role != 'Godfather'):
            await self.bot.send_message(ctx.message.author, "You're not the Godfather, but nice try")
            return
        elif (not (await self.userisalive(user)) ):
            await self.bot.send_message(ctx.message.author, "That user is already dead, or is not in the game")
            return
        for player in self.players:
            if (player.user.id == ctx.message.author.id):
                # overloading lynchchoice to function for mafiakill
                player.lynchchoice = user
                await self.bot.send_message(ctx.message.author, user.mention + " has been chosen for murdering")
    
    @commands.command(pass_context=True)
    async def doctorsave(self, ctx, user : discord.Member = None):
        """ Allows the doctor(s) to save one player per night. Usable only by the Doctor role"""
        role = await self.getuserrole(ctx.message.author)
        if (role != 'Doctor'):
            await self.bot.send_message(ctx.message.author, "How valiant, but you're not actually the doctor")
            return
        elif (not (await self.userisalive(user)) ):
            await self.bot.send_message(ctx.message.author, "You can't save someone who's already dead or not playing the game")
            return
        for player in self.players:
            if (player.user.id == ctx.message.author.id):
                # overloading lynchchoice to function for doctorsave
                player.lynchchoice = user 
                await self.bot.send_message(ctx.message.author, user.mention + " has been chosen for saving")
    
    @commands.command(pass_context=True)
    async def detectivefind(self, ctx, user : discord.Member = None):
        """ Allows the detective(s) to select which player they want to research"""
        role = await self.getuserrole(ctx.message.author)
        if (role != 'Detective'):
            await self.bot.send_message(ctx.message.author, "Sorry, you're not much of a sleuth")
            return
        elif (not (await self.userisalive(user)) ):
            await self.bot.send_message(ctx.message.author, "You're trying to detect someone who's dead or not playing the game")
            return
        for player in self.players:
            if (player.user.id == ctx.message.author.id):
                #overloading lynchchoice to function for detectivefind
                player.lynchchoice = user
                await self.bot.send_message(ctx.message.author, user.mention + " has been chosen for sleuthing")
    
    # !~~~~~~~~~~~~~~~
    # Internal methods
    # !~~~~~~~~~~~~~~~
    
    async def daystart(self):
        """start a new day"""
        if (await self.checkconditions()):
            return
        else:
            #reset lynch choices
            for player in self.players:
                player.lynchchoice = None
            self.gamestate = GameStates.DAY
            self.day += 1
            await self.bot.say( 'A new day is upon us, and with it comes death.\n'
                                'It\'s lynching time motherfuckers.')
    
    async def checkconditions(self):
        """Check win conditions"""
        #if there are no mafia left, then civs win
        mafiacount = 0
        civcount = 0
        for player in self.players:
            if (not player.isAlive):
                pass
            elif (player.team == 'Mafia'):
                mafiacount += 1
            elif (player.team == 'Civilian'):
                civcount += 1
        if (mafiacount == 0):
            self.gamestate = GameStates.END
            await self.bot.say("The game is over! The civilians have successfully discovered and lynched the mafiosos, and saved the town!")
            return True
        elif (civcount == 0):
            self.gamestate = GameStates.END
            await self.bot.say("The game is over! The mafia has successfully killed all civilians and taken control of the town!")
            return True
        else:
            return False
            
    async def userisalive(self, user : discord.Member):
        """Check if user is in the players list and is alive"""
        for player in self.players:
            if (player.user.id == user.id):
                return True
        return False
        
    async def getuserrole(self, user : discord.Member):
        """Gets the player role based off user id"""
        for player in self.players:
            if (player.user.id == user.id):
                return player.role
        return "error"
    
    async def getuserteam(self, user : discord.Member):
        """Gets the player team based off user id"""
        for player in self.players:
            if (player.user.id == user.id):
                return player.team
        return "error"
    
    async def commitlynch(self):
        """Execute the lynch. Returns True on successful lynch/nolynch, false otherwise"""
        # use a dictionary to tally lynch counts
        playerdict = {}
        playertotal = 0
        for player in self.players:
            if(player.isAlive):
                playertotal += 1
                playerdict[player.user.id] = 0
        # build the lynch tally
        for lyncher in self.players:
            if lyncher.lynchchoice == None:
                pass
            else:
                playerdict[lyncher.lynchchoice.id] += 1
        # do a pass through to determine the highest voted player
        highestcount = 0
        highestplayerid = 0
        morethanone = False
        for playerid, votecount in playerdict.items():
            if (votecount == highestcount):
                morethanone = True
            elif (votecount > highestcount):
                morethanone = False
                highestcount = votecount
                highestplayerid = playerid
        if (highestcount == 0):
            await self.bot.say('There was a unanimous vote to nolynch tonight. How civil of you all!')
            return True
        if (self.lynchmode == LynchModes.MAJORITY and highestcount < playertotal/2):
            await self.bot.say("A majority on who to lynch was not achieved. No lynch tonight")
            return True
        if (morethanone):
            await self.bot.say('There was a tie for who to lynch. Please resolve this before continuing!')
            return False
        # do one last pass to kill the lynched player
        for player in self.players:
            if (player.user.id == highestplayerid):
                player.isAlive = False
                player.causeOfDeath = "Lynched on day " + str(self.day)
                await self.bot.say(player.user.mention + ' has been lynched')
                return True
        await self.bot.say('Something went wrong. Returning to day cycle, no lynch occured')
        return False

def setup(bot):
    bot.add_cog(Mafia(bot))
