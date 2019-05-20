#!/usr/local/bin/python3
from datetime import datetime
import discord
from discord.ext import commands
import json
import pytz
import sqlite3
from twitter import Api
from twitter import TwitterError

with open("config.json") as f:
    config = json.loads(f.read())

consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]

class Twitter(commands.Cog):
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.api = Api(consumer_key=consumerKey, consumer_secret=consumerSecret,
        access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
        self.localTimeZone = pytz.timezone('Europe/Oslo')
        self.timeFormat = '%d %b %Y' + ' at ' + '%H:%M' + ' Central European'
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}

    def check_command_disabled(self, guild):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings['commands_disabled'], self.table), (guild.id,))
            commands_disabled = c.fetchone()
        conn.close()
        return(commands_disabled[0] == 0)

    @commands.command(pass_context=True)
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def twitter(self, ctx, stebenTwitterId=962385627663695872):
        if not self.check_command_disabled(ctx.message.guild):
            return(await ctx.say("This command is disabled"))

        try:
            tweetJSON = self.api.GetUserTimeline(user_id=stebenTwitterId, count=1, exclude_replies=True)[0]
        except TwitterError as e:
            return(await ctx.send(str(e)))

        tweetObject = json.loads(str(tweetJSON))

        embedTweet = discord.Embed(
            title = "Go to tweet",
            description = tweetObject["text"],
            url = "https://twitter.com/{0}/status/{1}".format(tweetObject["user"]["screen_name"], tweetObject["id_str"]),
            color = 0x00aced
        )
        embedTweet.set_author(
            name = "{0} ({1})".format(tweetObject["user"]["screen_name"], tweetObject["user"]["name"]),
            url = "https://twitter.com/{}".format(tweetObject["user"]["screen_name"]),
            icon_url = tweetObject["user"]["profile_image_url"]
        )
        utcTime = datetime.strptime(tweetObject["created_at"][4:], '%b %d %H:%M:%S %z %Y')
        localTime = utcTime.astimezone(self.localTimeZone).strftime(self.timeFormat)
        embedTweet.set_footer(text = localTime)
        return(await ctx.send(embed=embedTweet))

def setup(bot):
    bot.add_cog(Twitter(bot))
