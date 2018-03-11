import discord
from discord.ext import commands

class Osu:

    def __init__(self, discordClient):
        self.bot = discordClient

def setup(bot):
    bot.add_cog(Osu(bot))