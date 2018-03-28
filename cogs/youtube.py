import datetime
#from datetime import datetime
import discord
from discord.ext import commands
import json
import pytz
import sqlite3
import urllib3
urllib3.disable_warnings()

with open("config.json") as f:
    config = json.loads(f.read())

yt_api_key = config["yt_api_key"]

class Youtube:
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.yt_api_key = yt_api_key
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

    def check_command_disabled(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings['commands_disabled'], self.table), (server.id,))
            commands_disabled = c.fetchone()
        conn.close()
        return(commands_disabled[0] == 0)

    @commands.command(pass_context=True)
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def youtube(self, ctx, stebenChannelId="UC554eY5jNUfDq3yDOJYirOQ", channelLink="https://www.youtube.com/channel/{}",videoLink="https://youtube.com/watch?v={}"):
        if not self.check_command_disabled(ctx.message.server):
            return(await self.bot.say("This command is disabled"))

        requestString ="https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={0}&maxResults=1&type=video&order=date&key={1}"
        imageUrl = "https://i.ytimg.com/vi/{}/maxresdefault.jpg"
        width = 16
        height = 9

        http = urllib3.PoolManager()

        try:
            r = http.request('GET', requestString.format(stebenChannelId, self.yt_api_key))
            yt_object = json.loads(r.data.decode("utf-8"))
        except ValueError as err:
            print("youtube:",err)
            return(await self.bot.say("Failed to decode JSON object: {}".format(err)))
        except Exception as err:
            print(err)
            return(await self.bot.say("Error {}".format(err)))

        embedVideo = discord.Embed(
            title = yt_object["items"][0]["snippet"]["title"],
            description = yt_object["items"][0]["snippet"]["description"],
            url = videoLink.format(yt_object["items"][0]["id"]["videoId"]),
            color = 0xff0000
        )

        embedVideo.set_image(url = imageUrl.format(yt_object["items"][0]["id"]["videoId"]))
        embedVideo.image.width = width
        embedVideo.image.height = height

        embedVideo.set_author(
            name = yt_object["items"][0]["snippet"]["channelTitle"],
            url = channelLink.format(stebenChannelId),
            icon_url = self.getChannelImage()
        )
        naiveTime = datetime.datetime.strptime(yt_object["items"][0]["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%S.000Z') #2017-10-28T01:29:51.000Z
        utcTime = pytz.utc.localize(naiveTime)
        localTime = utcTime.astimezone(self.localTimeZone).strftime(self.timeFormat)
        embedVideo.set_footer(text = localTime)
        return(await self.bot.send_message(ctx.message.channel, embed=embedVideo))

    def getChannelImage(self, username="destiny"):
        requestString="https://www.googleapis.com/youtube/v3/channels?part=snippet%2C+contentDetails&forUsername={0}&key={1}".format(username, self.yt_api_key)

        http = urllib3.PoolManager()
        try:
            r = http.request('GET', requestString.format(username, self.yt_api_key))
            yt_object = json.loads(r.data.decode("utf-8"))
            return(yt_object["items"][0]["snippet"]["thumbnails"]["default"]["url"])
        except ValueError as err:
            print("Image:",err)
            return("Failed to decode JSON object: {}".format(err))
        except Exception as err:
            print(err)
            return("Error {}".format(err))

def setup(bot):
    bot.add_cog(Youtube(bot))