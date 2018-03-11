from discord.ext import commands
from twitch import TwitchClient
import json

with open("config.json") as f:
    config = json.loads(f.read())

clientId = config["twitch_client_id"]

class Twitch():

    def __init__(self, discordClient):
        self.bot = discordClient
        self.twitchClient = TwitchClient(client_id=clientId)

    @commands.command(pass_context=False)
    async def live(self, stebenChannelId=18074328, url="https://www.destiny.gg/bigscreen"):
        if self.disableCommands:
            return(await self.bot.say("This command is disabled"))
        stream = self.twitchClient.streams.get_live_streams(channel=stebenChannelId, stream_type="live")
        #channelName = self.twitchClient.channels.get_by_id(int(stebenChannelId)).name.capitalize()
        channelName = self.twitchClient.channels.get_by_id(stebenChannelId)
        print(channelName)
        if stream:
            return(await self.bot.say("{0} is live right now <:WhoahDude:309736750689943552> \n{1}".format(channelName, url)))
        else:
            return(await self.bot.say("{0} is not live right now 😦".format(channelName)))

def setup(bot):
    bot.add_cog(Twitch(bot))