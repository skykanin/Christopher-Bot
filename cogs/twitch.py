from discord.ext import commands
from twitch import TwitchClient
import json
import sqlite3

with open("config.json") as f:
    config = json.loads(f.read())

clientId = config["twitch_client_id"]

class Twitch(commands.Cog):

    def __init__(self, discordClient):
        self.bot = discordClient
        self.twitchClient = TwitchClient(client_id=clientId)
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

    
    @commands.command()
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def live(self, ctx, stebenChannelId=18074328, url="https://www.destiny.gg/bigscreen"):
        if not self.check_command_disabled(ctx.message.guild):
            return(await ctx.send("This command is disabled"))

        stream = self.twitchClient.streams.get_live_streams(channel=stebenChannelId, stream_type="live")

        if not stream:
            return(await ctx.send("{0} is not live right now 😦".format("Destiny")))

        game = stream[0]["game"]
        viewers = stream[0]["viewers"]
        name = stream[0]["channel"]["display_name"]
  
        return(await ctx.send("{0} is live right now, playing {1} with {2} viewers <:WhoahDude:309736750689943552> \n{3}".format(name, game, viewers, url)))

def setup(bot):
    bot.add_cog(Twitch(bot))
