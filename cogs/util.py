from datetime import datetime
import dice
import discord
from discord.ext import commands
import feedparser
import json
import pyimgur
import pytz
import random
import sys
import sqlite3
from time import strftime

with open("config.json") as f:
    config = json.loads(f.read())

client_id = config["imgur_client_id"]
client_secret = config["imgur_client_secret"]

class Util:
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.imgurClient = pyimgur.Imgur(client_id)
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}
    
    @commands.command()
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def ping(self, ctx):
        now = datetime.utcnow()
        delta = now - ctx.message.created_at
        return(await ctx.send('Pong! Took {}ms'.format(delta.microseconds // 1000)))

    @ping.error
    async def ping_error(self, ctx, error):
        return(await ctx.send(error))

    @commands.command()
    async def nc(self, ctx, timezone='America/New_York', url='http://feeds.feedburner.com/NakedCapitalism'):
        ncFeed = feedparser.parse(url)
        offset = pytz.timezone(timezone)
        todaysEntries = []

        for entry in ncFeed.entries:
            if datetime.now(tz=offset).timetuple().tm_yday == entry.published_parsed.tm_yday:
                todaysEntries.append(entry)

        if(len(todaysEntries) == 0):
            return(await ctx.send("No new posts today 😢"))

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
            text="Published on {}".format(datetime.now(tz=offset).strftime('%A EST time'))
        )

        for entry in todaysEntries:
            ncEmbed.add_field(
                name=entry.title,
                value=entry.feedburner_origlink,
                inline=False
            )

        try:
            return(await ctx.send(embed=ncEmbed))
        except Exception as e:
            print(e)

    def check_roll_channel(self, guild):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT roll_channel FROM {} WHERE guild_id=?".format(self.table), (guild.id,))
            guild_settings = c.fetchone()
        conn.close()
        return(guild_settings[0])

    @commands.command()
    @commands.cooldown(1,15.0,type=commands.BucketType.user)
    async def roll(self, ctx, arg, docs="https://github.com/borntyping/python-dice/blob/master/README.rst"):
        roll_channel = self.check_roll_channel(ctx.message.guild)

        if not roll_channel == ctx.message.channel.name:
            return(await ctx.send("You can only use this command in the {} channel".format(roll_channel)))

        try:
            result = dice.roll(str(arg))
            return(await ctx.send(result))
        except dice.DiceBaseException as e:
            return(await ctx.send("{0}\n\nIf you want the full documentation for the parser check this out:\n<{1}>".format(e.pretty_print(), docs)))
    
    @roll.error
    async def roll_error(self, ctx, error):
        return(await ctx.send(error))

    @commands.command()
    @commands.cooldown(1,10.0,type=commands.BucketType.user)
    async def rms(self, ctx, album_id="7K5Gcmh", imgur_link="https://imgur.com/a/7K5Gcmh"):
        rms_images = self.imgurClient.get_album(album_id).images
        rand_int = random.randint(0, len(rms_images)-1)
        rand_image = rms_images[rand_int].link

        image_embed = discord.Embed(title="Our GNU/Lord and GNU/Savior")
        image_embed.set_image(url=rand_image)

        return(await ctx.send(embed=image_embed))
    
    @rms.error
    async def roll_error(self, ctx, error):
        return(await ctx.send(error))

    @commands.command()
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
        return(await ctx.send(embed=embed))
    
    @commands.command()
    async def ts(self, ctx):
        return(await ctx.send("T Y P E    S A F E"))

    @commands.command()
    async def commands(self, ctx):
        return(await ctx.send("For a full list of all my commands and how to use them, checkout my github repository (https://github.com/skykanin/Christopher-Bot) README file"))

    async def on_message_delete(self, message):
        if message.content == "T Y P E    S A F E":
            await message.channel.send("T Y P E    S A F E")

def setup(bot):
    bot.add_cog(Util(bot))