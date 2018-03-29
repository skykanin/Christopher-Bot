import discord
from discord.ext import commands
import emoji
import math
from osuapi import OsuApi, ReqConnector, enums
import json
import sqlite3

class Osu:

    def __init__(self, discordClient):

        with open("config.json") as f:
            config = json.loads(f.read())

        self.bot = discordClient
        self.osuApi = OsuApi(config["osu_key"], connector=ReqConnector())
        self.modeMap = {'standard': enums.OsuMode.osu, 'mania': enums.OsuMode.mania}
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}

    def check_correct_channel(self, message):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings['osu_channel'], self.table), (message.server.id,))
            channel = c.fetchone()
        conn.close()
        return(not channel[0] == message.channel.name)

    @commands.group(pass_context=True)
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            return(await self.bot.say('Invalid subcommand for osu passed...'))

    @osu.command(pass_context=True)
    async def profile(self, ctx, profile, mode_arg="standard"):
        if self.check_correct_channel(ctx.message):
            return(await self.bot.say('You cannot use this command in this channel'))

        if mode_arg not in self.modeMap:
            return(await self.bot.say('Not a valid game mode'))
        else:
            result = self.osuApi.get_user(str(profile),mode=self.modeMap[mode_arg], event_days=31)

        if not result:
            return(await self.bot.say("User doesn't exist"))

        data = result[0] #get first and only result
        acc = str(math.ceil(data.accuracy*100)/100) + "%"
        lvl = str(math.ceil(data.level*100)/100)

        profile_embed = discord.Embed(
            url = "https://osu.ppy.sh/users/{}".format(data.user_id),
            color = 0xea1595
        )

        profile_embed.add_field(
            name = "Performance",
            value = "Global PP Rank: {0}\nPP: {1}\nAccuracy: {2}".format(data.pp_rank, data.pp_raw, acc),
            inline = True
        )

        profile_embed.add_field(
            name = "Experience",
            value = "Playcount: {0}\nLevel: {1}\n".format(data.playcount, lvl)
        )

        profile_embed.add_field(
            name = "Country",
            value = emoji.emojize("Country PP Rank: {0}\n:flag_{1}:"
                    .format(data.pp_country_rank, data.country.lower())
                ),
            inline = True
        )

        profile_embed.set_author(
            name = data.username,
            url = "https://osu.ppy.sh/users/{}".format(data.user_id),
            icon_url = "http://s.ppy.sh/a/{}".format(data.user_id)
        )

        return(await self.bot.send_message(ctx.message.channel, embed=profile_embed))
    
    @profile.error
    async def profile_error(self, error, ctx):
        return(await self.bot.send_message(ctx.message.channel, str(error).capitalize()))

def setup(bot):
    bot.add_cog(Osu(bot))