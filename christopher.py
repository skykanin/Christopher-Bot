#!/usr/local/bin/python3
import aiohttp
import discord
from discord.ext import commands
import json
from os import listdir
from os.path import isfile, join
import sys
import traceback

with open("config.json") as f:
    config = json.loads(f.read())

bot_description = "General purpose bot made with sweat and tears by skykanin"
bot_prefix = config["prefix"]

bot = commands.Bot(description=bot_description, command_prefix=bot_prefix, pm_help=None, help_attrs=dict(hidden=True))

# this specifies what extensions to load when the bot starts up (from this directory)
cogs_dir = "cogs"

extensions = (
    'cogs.admin',
    'cogs.config',
    'cogs.log',
    'cogs.osu',
    'cogs.twitch',
    'cogs.twitter',
    'cogs.util',
    'cogs.youtube',
)

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
        await bot.add_reaction(message, godstiny)
    if "hot coco" in content:
        await bot.add_reaction(message, pepeComfy)       
    await bot.process_commands(message)

""" @bot.event
async def on_error(event):
    bot.connect(reconnect=True) """

@bot.event
async def on_command_error(error, ctx):
    return(await bot.send_message(ctx.message.channel, error))

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            print('Failed to load extension {extension}.')
            traceback.print_exc()
    bot.run(config["token"])