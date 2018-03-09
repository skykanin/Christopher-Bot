#!/usr/bin/python3.6
import discord
from discord.ext import commands
from discord.ext.commands import Bot


class Logger:
    
    def __init__(self, bot):
        self.bot = bot

    #@Bot.event
    async def on_server_join(self, server):
        logs = next((channel for channel in server.channels if channel.name == "logs"), None)
        if not logs:
            try:
                everyone_perms = discord.PermissionOverwrite(write_messages=False)
                everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)

                await self.bot.create_channel(server, 'logs', everyone, type=discord.ChannelType.text)
            except Exception as e:
                print("create_channel:",e)

    #@Bot.event
    async def on_message_delete(self, message):
        embedDeletedMessage = discord.Embed(
            title="Deleted from #{}:".format(message.channel.name),
            description=message.content,
            timestamp=message.timestamp,
            colour=0xff0000
        )
        embedDeletedMessage.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        embedDeletedMessage.set_footer(
            text="Deleted message"
        )
        logsChannel = next((channel for channel in message.server.channels if channel.name == "logs"), None)
        try:
            await self.bot.send_message(logsChannel, embed=embedDeletedMessage)
        except Exception as e:
            print(e)

    #@Bot.event
    async def on_message_edit(self, before,after):
        if before.content == after.content:
            return

        embedEditedMessage = discord.Embed(
            title="Before:",
            description=before.content,
            timestamp=after.timestamp,
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
        logsChannel = next((channel for channel in after.server.channels if channel.name == "logs"), None)
        try:
            await self.bot.send_message(logsChannel, embed=embedEditedMessage)
        except Exception as e:
            print(e)