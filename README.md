# Mafianaros - A discord cog built on top of Red. 
This discord bot uses channel commands and pms to manage a game of mafia, removing the need for a host in a typical game of mafia and allowing everyone to join the fun :)

## Mafianaros commands
* !addciv
* !addmafia
* !addplayer
* !dayend
* !detectivefind
* !doctorsave
* !lynch
* !lynchlist
* !mafiahelp
* !mafiakill
* !mafiamsg
* !mafiareset
* !mafiastart
* !mafiastatus
* !nightend
* !savegame
* !setlynchmode

## Mafianaros how-to
First load the cog into your bot using !load mafia.

To start a game, the host will type !mafiareset. This initializes the game, and gives you a to do list: add roles for mafia, add players, and set the lynch mode. To find the available roles, type !mafiahelp. Lynch mode is either plurality, meaning the player who receives the most lynch votes is out, or majority, meaning a player is only lynched when he has a majority votes on him.
If at any time you're confused on what to do, try typing !mafiahelp or !mafiastatus.

When adding roles, you may add as many mafia and civ roles as you'd like. If there are fewer roles than players, the remaining roles will be autofilled with civilians.

Once roles and players have been added, start the game with !mafiastart. This will send out roles to everyone and begin the game at daytime.

As with a typical game of mafia, daytime is when you decide who to lynch. Everyone is public here, and lynches will be decided in the main text channel. The pertinent commands here are !lynch <player>, !nolynch, and !lynchlist. Note that if a <Player> name has spaces, you must use quotations (e.g. !lynch "Big Dan")
Once lynching (or nolynching) has been decided, type the !dayend command. The lynch votes will be tallied and someone may be lynched from the game.

At this point, nighttime commences, and those with special roles will be prompted to select someone to hurt, heal, investigate, and the mafia will decide collectively who to try and kill. 
The mafia can message each other by sending private messages to Mafianaros using !mafiamsg <message>. Similar to lynching, the mafia will decide who to kill using !mafiakill <playername>.
Civilians with special roles will similarly be prompted to PM Mafianaros, and have special commands such as !detectivefind <player> and !doctorsave <player>.

Once nighttime activities have been concluded, end the nighttime with !nightend. A public message will be sent to the group about what transpired at night, and daytime will commence once again.

And that's it. Once all the civilians or all the mafia have been eliminated, the game will end with a win for one team. I hope you enjoy using this bot :)


# Red - A fully customizable Discord bot
#### *Music, admin, trivia, fun commands and much more!*
[<img src="https://img.shields.io/badge/Support-me!-orange.svg">](https://www.patreon.com/Twentysix26)  [<img src="https://img.shields.io/badge/discord-py-blue.svg">](https://github.com/Rapptz/discord.py) [<img src="https://discordapp.com/api/guilds/133049272517001216/widget.png?style=shield">](https://discord.gg/red) [![Build Status](https://api.travis-ci.org/Cog-Creators/Red-DiscordBot.svg?branch=develop)](https://travis-ci.org/Cog-Creators/Red-DiscordBot) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**Red** is a fully modular bot – meaning all features and commands can be enabled/disabled to your liking, making it completely customizable.  
This is also a *self-hosted bot* – meaning you will need to host and maintain your own instance. You can turn Red into an admin bot, music bot, trivia bot, new best friend or all of these together!  
[Installation is easy](https://twentysix26.github.io/Red-Docs/), and you do NOT need to know anything about coding! Aside from installation and updating, every part of the bot can be controlled from within Discord.

The default set of modules includes and is not limited to:
* Moderation features (kick/ban/softban/hackban, mod-log, filter, chat cleanup)
* Trivia (lists are included and can be easily added)
* Music features (YouTube, SoundCloud, local files, playlists, queues)
* Stream alerts (Twitch, Mixer, Smashcast)
* Slot machines
* Custom commands
* Imgur/gif search

Additionally, other modules (cogs) can be easily found and added from our growing community of cog repositories. Including:
* Cleverbot integration (talk to Red and she talks back)
* Loggers
* Welcome messages setup
* Reminders
* Raffles
* Leveler (increase levels for server participation)
* Sound effects
* And much, much more!

Feel free to take a [peek](https://cogs.red/)!

# Installation

The installation process is straightforward; all major platforms are supported: 
* [Windows](https://twentysix26.github.io/Red-Docs/red_install_windows/)
* [Linux](https://twentysix26.github.io/Red-Docs/red_install_linux/)
* [macOS](https://twentysix26.github.io/Red-Docs/red_install_mac/)

Read the [getting started](https://twentysix26.github.io/Red-Docs/red_getting_started/) guide to quickly learn how to use Red.  

If you have any other questions, feel free to explore the [Docs](https://twentysix26.github.io/Red-Docs/) for guidance.

If [*after reading the guides*](https://twentysix26.github.io/Red-Docs/) you are still experiencing issues that are not listed on [this page](https://twentysix26.github.io/Red-Docs/red_guide_troubleshooting/) or in the [FAQs](https://twentysix26.github.io/Red-Docs/red_faq/), feel free to join the [official server](https://discord.gg/red) for help.  
Have fun!

# Join the community!

Red is in continuous development, and it’s supported by an active community which produces new content (cogs/plugins) for everyone to enjoy. New features are constantly added. If you can’t [find](https://cogs.red/) what you’re looking for, we are open to suggestions! Stay tuned by [joining the official server](https://discord.gg/red)!

# License

Released under the [GNU GPL v3](LICENSE).

*Red is named after the main character of "Transistor", a videogame by [Supergiant Games](https://www.supergiantgames.com/games/transistor/)*
