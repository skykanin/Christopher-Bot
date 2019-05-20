#!/usr/bin/python3
import discord
from discord.ext import commands
import sqlite3

class Admin(commands.Cog):
    def __init__(self, discordClient):
        self.bot = discordClient
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}

    def check_for_admin_role(self, ctx):
        # Get admin role name for specific guild
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings['admin_role'], self.table), (ctx.message.guild.id,))
            guild_role = c.fetchone()[0]
        conn.close()

        # Check if user has the guild admin role  
        for role in ctx.message.author.roles:
            if role.name == guild_role.title():
                return True
        return False

    async def mute_function(self, ctx):
        toMute = ctx.message.content.split(' ')[0] == "!mute"
        serverRoles = ctx.message.guild.roles

        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command <:OverRustle:286162736625352716>"))
        
        if not ctx.message.mentions:
            if toMute:
                return(await ctx.send("You haven't passed an argument. The command is: !mute <mentionUser>"))
            else:
                return(await ctx.send("You haven't passed an argument. The command is: !unmute <mentionUser>"))
        else:
            mentionedMember = ctx.message.mentions[0]
            memberToToggleMute = ctx.message.guild.get_member(mentionedMember.id)
            mutedRole = self.get_role(serverRoles, 'Muted')
            forbiddenMessage = "I don't have permission to do that! <:pepoS:350644750191165441>"
            failedMessage = "Failed to {} role! <:pepoS:350644750191165441>"
            returnMessage = "User {0} is now {1}"

            if toMute:
                if mutedRole in memberToToggleMute.roles:
                    return(await ctx.send("{} already has the Muted role".format(mentionedMember)))
                try:
                    await memberToToggleMute.add_roles(mutedRole)
                except discord.Forbidden:
                    return(await ctx.send(forbiddenMessage))
                except discord.HTTPException:
                    return(await ctx.send(failedMessage.format("add")))
                return(await ctx.send(returnMessage.format(mentionedMember, "muted")))
            else:
                if mutedRole not in memberToToggleMute.roles:
                    return(await ctx.send("{} does not have the Muted role".format(mentionedMember)))
                try:
                    await memberToToggleMute.remove_roles(mutedRole)
                except discord.Forbidden:
                    return(await ctx.send(forbiddenMessage))
                except discord.HTTPException:
                    return(await ctx.send(failedMessage.format("remove")))
                return(await ctx.send(returnMessage.format(mentionedMember, "unmuted")))
    
    @commands.command()
    async def mute(self, ctx): #cuck shitters
        await self.mute_function(ctx) 

    @commands.command()
    async def unmute(self, ctx): #uncuck shitters
        await self.mute_function(ctx)

    def get_role(self, server_roles, target_name):
        return next((x for x in server_roles if x.name == target_name), None)

def setup(bot):
    bot.add_cog(Admin(bot))
