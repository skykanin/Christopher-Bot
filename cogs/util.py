from datetime import datetime
import dice
import discord
from discord.ext import commands
import feedparser
import sys
import random
import sqlite3

class Util:
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}
    
    @commands.command(pass_context=True)
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def ping(self, ctx):
        now = datetime.utcnow()
        delta = now - ctx.message.timestamp
        return(await self.bot.say('Pong! Took {}ms'.format(delta.microseconds // 1000)))

    """ @ping.error
    async def ping_error(self, error, ctx):
        return(await self.bot.say(error)) """

    @commands.command(pass_context=True)
    async def nc(self, ctx, url='http://feeds.feedburner.com/NakedCapitalism'):
        ncFeed = feedparser.parse(url)
        todaysEntries = []
        for entry in ncFeed.entries:
            if datetime.utcnow().timetuple().tm_yday == entry.published_parsed.tm_yday:
                todaysEntries.append(entry)

        if(len(todaysEntries) == 0):
            return(await self.bot.say("No new posts today 😢"))

        ncEmbed = discord.Embed(
            title="Todays posts",
            colour=0xE86530
        )
        
        ncEmbed.set_author(
            name="Naked Capitalism",
            url="https://www.nakedcapitalism.com",
            icon_url="https://i.imgur.com/Ozeqkol.png"
        )

        ncEmbed.set_footer(
            text="Published on {}".format(datetime.utcnow().strftime('%A UTC time'))
        )

        for entry in todaysEntries:
            ncEmbed.add_field(
                name=entry.title,
                value=entry.feedburner_origlink,
                inline=False
            )

        try:
            return(await self.bot.say(embed=ncEmbed))
        except Exception as e:
            print(e)

    def check_roll_channel(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT roll_channel FROM {} WHERE guild_id=?".format(self.table), (server.id,))
            guild_settings = c.fetchone()
        conn.close()
        return(guild_settings[0])

    @commands.command(pass_context=True)
    @commands.cooldown(1,15.0,type=commands.BucketType.user)
    async def roll(self, ctx, arg, docs="https://github.com/borntyping/python-dice/blob/master/README.rst"):
        roll_channel = self.check_roll_channel(ctx.message.server)

        if not roll_channel == ctx.message.channel.name:
            return(await self.bot.say("You can only use this command in the {} channel".format(roll_channel)))

        try:
            result = dice.roll(str(arg))
            return(await self.bot.say(result))
        except dice.DiceBaseException as e:
            return(await self.bot.say("{0}\n\nIf you want the full documentation for the parser check this out:\n<{1}>".format(e.pretty_print(), docs)))
        
    @commands.command(pass_context=True)
    async def about(self, ctx):
        embed = discord.Embed(
            title = "I am Christopher Bot",
            description = "I am an administration bot made by Skykanin, written in Python using the discord.py API. If you want to look at my code check out my github repository and if you find any bugs bother Skykanin about it.",
            url = "https://github.com/skykanin/Christopher-Bot",
            color = 0xffffff
        )
        embed.set_author(
            name = "skykanin",
            url = "https://github.com/skykanin",
            icon_url = "https://avatars0.githubusercontent.com/u/3789764?s=460&v=4"
        )
        return(await self.bot.send_message(ctx.message.channel, embed=embed))
    
    @commands.command(pass_context=False)
    async def commands(self):
        return(await self.bot.say("For a full list of all my commands and how to use them, checkout my github repository (https://github.com/skykanin/Christopher-Bot) README file"))

def setup(bot):
    bot.add_cog(Util(bot))