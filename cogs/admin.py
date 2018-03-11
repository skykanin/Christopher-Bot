#!/usr/bin/python3
import discord
from discord.ext import commands

class Admin:
    
    def __init__(self, discordClient):
        self.bot = discordClient
        self.adminRoleName = "Admin"

    async def mute_function(self, ctx):
        if self.disableCommands:
            return(await self.bot.say("This command is disabled"))
        
        toMute = ctx.message.content.split(' ')[0] == "!mute"

        hasAdminRole = False
        serverRoles = ctx.message.server.roles

        for e in ctx.message.author.roles:
            if e.name == self.adminRoleName:
                hasAdminRole = True
                break

        if not hasAdminRole:
            return(await self.bot.say("You don't have permission to use this command <:OverRustle:286162736625352716>"))
        
        if not ctx.message.mentions:
            if toMute:
                return(await self.bot.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
            else:
                return(await self.bot.say("You haven't passed an argument. The command is: !unmute <mentionUser>"))
        else:
            mentionedMember = ctx.message.mentions[0]
            memberToToggleMute = ctx.message.server.get_member(mentionedMember.id)
            mutedRole = self.get_role(serverRoles, 'Muted')
            forbiddenMessage = "I don't have permission to do that! <:pepoS:350644750191165441>"
            failedMessage = "Failed to {} role! <:pepoS:350644750191165441>"
            returnMessage = "User {0} is now {1}"

            if toMute:
                if mutedRole in memberToToggleMute.roles:
                    return(await self.bot.say("{} already has the Muted role".format(mentionedMember)))
                try:
                    print("Roles to add", mutedRole)
                    await self.bot.add_roles(memberToToggleMute, mutedRole)
                    print("Roles after addition", memberToToggleMute.roles)
                except discord.Forbidden:
                    return(await self.bot.say(forbiddenMessage))
                except discord.HTTPException:
                    return(await self.bot.say(failedMessage.format("add")))
                return(await self.bot.say(returnMessage.format(mentionedMember, "muted")))
            else:
                if mutedRole not in memberToToggleMute.roles:
                    return(await self.bot.say("{} does not have the Muted role".format(mentionedMember)))
                try:
                    print("Roles to remove:", mutedRole)
                    await self.bot.remove_roles(memberToToggleMute, mutedRole)
                    print("Roles after removal", memberToToggleMute.roles)
                except discord.Forbidden:
                    return(await self.bot.say(forbiddenMessage))
                except discord.HTTPException:
                    return(await self.bot.say(failedMessage.format("remove")))
                return(await self.bot.say(returnMessage.format(mentionedMember, "unmuted")))
    
    @commands.command(pass_context=True)
    async def mute(self, ctx): #cuck shitters
        await self.mute_function(ctx) 

    @commands.command(pass_context=True)
    async def unmute(self, ctx): #uncuck shitters
        await self.mute_function(ctx)

    def get_role(self, server_roles, target_name):
        return next((x for x in server_roles if x.name == target_name), None)

def setup(bot):
    bot.add_cog(Admin(bot))