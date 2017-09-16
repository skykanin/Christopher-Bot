import discord
import asyncio
import json
from discord.ext import commands

config = json.loads(open("config.json", "r").read())

bot_description = "Admin bot"
bot_prefix = config["prefix"]

client = commands.Bot(description=bot_description, command_prefix=bot_prefix)

list_of_strings = ['add a reaction', 'add rxn', 'ok']

@client.event
async def on_ready():
    print("Logged in")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print(discord.__version__)


@client.command()
async def ping(*args):
    return(await client.say("Pong!"))

@client.command(pass_context=True)
async def mute(ctx):
    return(await client.say("User {} is now muted".format(ctx.message.content[5:])))

    
@client.event
async def on_message(message):
    if message.content.lower() in list_of_strings:
        await client.add_reaction(message, "👌")
    await client.process_commands(message)

client.run(config["token"])