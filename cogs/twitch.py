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
        stream = self.twitchClient.streams.get_live_streams(channel=stebenChannelId, stream_type="live")
        game = stream[0]["game"]
        viewers = stream[0]["viewers"]
        name = stream[0]["channel"]["display_name"]
        if stream:
            return(await self.bot.say("{0} is live right now, playing {1} with {2} viewers <:WhoahDude:309736750689943552> \n{3}".format(name, game, viewers, url)))
        else:
            return(await self.bot.say("{0} is not live right now 😦".format(channelName)))

def setup(bot):
    bot.add_cog(Twitch(bot))