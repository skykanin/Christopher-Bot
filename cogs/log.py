#!/usr/bin/python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot


class Logger(commands.Cog):
    
    def __init__(self, discordClient):
        self.bot = discordClient
        
    async def on_guild_join(self, guild):
        logs = next((channel for channel in guild.channels if channel.name == "logs"), None)
        if not logs:
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(write_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }

                await guild.create_text_channel('logs', overwrites, type=discord.ChannelType.text)
            except Exception as e:
                print("create_channel:",e)

    async def on_message_delete(self, message):
        embedDeletedMessage = discord.Embed(
            title="Deleted from #{}:".format(message.channel.name),
            description=message.content,
            timestamp=message.created_at,
            colour=0xff0000
        )
        embedDeletedMessage.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        embedDeletedMessage.set_footer(
            text="Deleted message"
        )
        logsChannel = next((channel for channel in message.guild.channels if channel.name == "logs"), None)
        try:
            await logsChannel.send(embed=embedDeletedMessage)
        except Exception as e:
            print(e)

    async def on_message_edit(self, before,after):
        if before.content == after.content:
            return

        embedEditedMessage = discord.Embed(
            title="Before:",
            description=before.content,
            timestamp=after.created_at,
            colour=0x0000ff
        )
        embedEditedMessage.add_field(
            name="After:",
            value=after.content,
            inline=True
        )
        embedEditedMessage.set_author(
            name=after.author.name,
            icon_url=after.author.avatar_url
        )
        embedEditedMessage.set_footer(
            text="Edited message"
        )
        logsChannel = next((channel for channel in after.guild.channels if channel.name == "logs"), None)
        try:
            await logsChannel.send(embed=embedEditedMessage)
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Logger(bot))
