#!/usr/bin/python3
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from twitch import TwitchClient
from botCommands import BotCommands
import calendar
import datetime
import discord
import json
import pytz
import random
import twitter

with open("config.json") as f:
    config = json.loads(f.read())

bot_description = "Admin bot"
bot_prefix = config["prefix"]
consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]
clientId = config["twitch_client_id"]
yt_api_key = config["yt_api_key"]

client = Bot(description=bot_description, command_prefix=bot_prefix)
api = twitter.Api(consumer_key=consumerKey, consumer_secret=consumerSecret,
    access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
twitchClient = TwitchClient(client_id=clientId)
client.add_cog(BotCommands(client, api, twitchClient, yt_api_key))

@client.event
async def on_ready():
    print("Logged in")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print(discord.__version__)
    await client.change_presence(game=discord.Game(name="with Alan"))

@client.event
async def on_message(message, list_of_strings=['best lang', 'what is the best programming language?', 'what language is the best?']):

    content = message.content.lower()
    godstiny = ":GODSTINY:347438305601912833"
    pepeComfy = ":pepeComfy:372014257044193302"

    if content in list_of_strings:
        await client.add_reaction(message, "🐢")
        await client.add_reaction(message, "🚀")
    if "the power of js" in content:
        await client.add_reaction(message, godstiny)
    if "hot coco" in content:
        await client.add_reaction(message, pepeComfy)       
    await client.process_commands(message)

@client.event
async def on_server_join(server):
    logs = next((channel for channel in server.channels if channel.name == "logs"), None)
    if not logs:
        try:
            everyone_perms = discord.PermissionOverwrite(write_messages=False)
            everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)

            await client.create_channel(server, 'logs', everyone, type=discord.ChannelType.text)
        except Exception as e:
            print("create_channel:",e)

@client.event
async def on_message_delete(message):
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
        await client.send_message(logsChannel, embed=embedDeletedMessage)
    except Exception as e:
        print(e)

@client.event
async def on_message_edit(before,after):
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
        await client.send_message(logsChannel, embed=embedEditedMessage)
    except Exception as e:
        print(e)

@client.event
async def on_error(event):
    client.connect(reconnect=True)

if __name__ == "__main__":
    client.run(config["token"])