from datetime import datetime
from discord.ext import commands
import feedparser

class Util:
    
    def __init__(self, discordClient):
        self.bot = discordClient
    
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - ctx.message.timestamp
        return(await self.bot.say('Pong! Took {}ms'.format(delta.microseconds // 1000)))

    @commands.command(pass_context=True)
    async def nc(self, ctx, url='http://feeds.feedburner.com/NakedCapitalism'):
        ncFeed = feedparser.parse(url)
        todaysEntries = []
        for entry in ncFeed.entries:
            if datetime.datetime.utcnow().timetuple().tm_yday == entry.published_parsed.tm_yday:
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
            text="Published on {}".format(datetime.datetime.utcnow().strftime('%A UTC time'))
        )

        for entry in todaysEntries:
            ncEmbed.add_field(
                name=entry.title,
                value=entry.feedburner_origlink,
                inline=False
            )

        try:
            return(await self.bot.send_message(ctx.message.channel, embed=ncEmbed))
        except Exception as e:
            print(e)
        
    @commands.command(pass_context=True)
    async def roll(self, ctx):
        string = ctx.message.content
        maxVal = 100
    
        if string == '!roll':
            return(await self.bot.say("{}".format(random.randint(1,maxVal))))
        
        diceFaces = string.split(" ",1)[1]
        
        try:
            diceFacesValue = int(diceFaces)
        except Exception:
            return(await self.bot.say("Bad input, argument must be an integer"))

        print(diceFacesValue)
        if diceFacesValue > 0 and diceFacesValue <= maxVal:
            return(await self.bot.say("{}".format(random.randint(1,diceFacesValue))))

        return(await self.bot.say("Number must be between 1 and 100. Example of correct use !roll 6"))

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