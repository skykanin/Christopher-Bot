import discord
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
    hasRole = False
    serverRoles = ctx.message.server.roles
    for e in ctx.message.author.roles:
        if e.name == "Admin":
            hasRole = True
    if hasRole and ctx.message.mentions:
        rolesToAdd = get_role(serverRoles, 'Muted')
        memberToMute = ctx.message.server.get_member(ctx.message.mentions[0].id)
        await client.add_roles(memberToMute, rolesToAdd)
        return(await client.say("User {} is now muted".format(ctx.message.mentions[0])))
    elif hasRole and not ctx.message.mentions:
        return(await client.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
    else:
        return(await client.say("You don't have permission to use this command"))

def get_role(server_roles, target_name):
    for each in server_roles:
        if each.name == target_name:
            return each
    print("Didn't find role")
    return None
    
@client.event
async def on_message(message):
    if message.content.lower() in list_of_strings:
        await client.add_reaction(message, "👌")
    await client.process_commands(message)

client.run(config["token"])