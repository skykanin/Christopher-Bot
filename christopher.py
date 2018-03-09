#!/usr/bin/python3.6
import discord
from discord.ext import commands

from datetime import datetime
from twitch import TwitchClient

from botCommands import BotCommands
from log import Logger

import calendar
import datetime
import json
import pytz
import random
import twitter

with open("config.json") as f:
    config = json.loads(f.read())

bot_description = "General purpose bot made with sweat and tears by skykanin"
bot_prefix = config["prefix"]
consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]
clientId = config["twitch_client_id"]
yt_api_key = config["yt_api_key"]

bot = commands.Bot(description=bot_description, command_prefix=bot_prefix)

api = twitter.Api(consumer_key=consumerKey, consumer_secret=consumerSecret,
    access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
twitchClient = TwitchClient(client_id=clientId)

bot.add_cog(BotCommands(bot, api, twitchClient, yt_api_key))
bot.add_cog(Logger(bot))

@bot.event
async def on_ready():
    print("Logged in")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print(discord.__version__)
    await bot.change_presence(game=discord.Game(name="with Alan"))

@bot.event
async def on_message(message, list_of_strings=['best lang', 'what is the best programming language?', 'what language is the best?']):

    content = message.content.lower()
    godstiny = ":GODSTINY:347438305601912833"
    pepeComfy = ":pepeComfy:372014257044193302"

    if content in list_of_strings:
        await bot.add_reaction(message, "🐢")
        await bot.add_reaction(message, "🚀")
    if "the power of js" in content:
        await clibotent.add_reaction(message, godstiny)
    if "hot coco" in content:
        await bot.add_reaction(message, pepeComfy)       
    await bot.process_commands(message)

@bot.event
async def on_error(event):
    bot.connect(reconnect=True)

if __name__ == "__main__":
    bot.run(config["token"])