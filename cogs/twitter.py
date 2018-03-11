from datetime import datetime
import discord
from discord.ext import commands
import json
import pytz
import twitter
from twitter.error import TwitterError

with open("config.json") as f:
    config = json.loads(f.read())

consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]

class Twitter:
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.api = twitter.Api(consumer_key=consumerKey, consumer_secret=consumerSecret,
        access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
        self.localTimeZone = pytz.timezone('Europe/Oslo')
        self.timeFormat = '%d %b %Y' + ' at ' + '%H:%M' + ' Central European'

    @commands.command(pass_context=True)
    async def twitter(self, ctx, stebenTwitterId=962385627663695872):
        if self.disableCommands:
            return(await self.bot.say("This command is disabled"))

        try:
            tweetJSON = self.api.GetUserTimeline(user_id=stebenTwitterId, count=1, exclude_replies=True)[0]
        except TwitterError as e:
            return(await self.bot.send_message(ctx.message.channel, str(e)))

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
        utcTime = datetime.datetime.strptime(tweetObject["created_at"][4:], '%b %d %H:%M:%S %z %Y')
        localTime = utcTime.astimezone(self.localTimeZone).strftime(self.timeFormat)
        embedTweet.set_footer(text = localTime)
        return(await self.bot.send_message(ctx.message.channel, embed=embedTweet))

def setup(bot):
    bot.add_cog(Twitter(bot))
