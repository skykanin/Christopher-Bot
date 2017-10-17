import discord
import json
import twitter
from discord.ext import commands

config = json.loads(open("config.json", "r").read())

bot_description = "Admin bot"
bot_prefix = config["prefix"]

consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["accessTokenSecret"]

api = twitter.Api(consumer_key=[consumerKey], consumer_secret=[consumerSecret], access_token_key=[accessTokenKey], access_token_secret=[accessTokenSecret])
client = commands.Bot(description=bot_description, command_prefix=bot_prefix)

list_of_strings = ['best lang', 'what is the best programming language?', 'what language is the best?']
dict_of_roles = {}

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
async def mute(ctx): #fuck shitters
    hasRole = False
    serverRoles = ctx.message.server.roles
    for e in ctx.message.author.roles:
        if e.name == "Admin":
            hasRole = True
    if hasRole and ctx.message.mentions:
        rolesToAdd = get_role(serverRoles, 'Muted')
        memberToMute = ctx.message.server.get_member(ctx.message.mentions[0].id)
        try:
            await client.remove_roles(memberToMute, *memberToMute.roles)
        except discord.Forbidden:
            return(await client.say("I don't have permission to do that! <:monkaS:356891254006611970>"))
        dict_of_roles[memberToMute.id] = memberToMute.roles #Adds member to the mute list
        print(dict_of_roles)
        await client.add_roles(memberToMute, rolesToAdd)
        return(await client.say("User {} is now muted".format(ctx.message.mentions[0])))
    elif hasRole and not ctx.message.mentions:
        return(await client.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
    else:
        return(await client.say("You don't have permission to use this command <:FeelsRageMan:356757133393657867>"))

@client.command(pass_context=True)
async def unmute(ctx): #uncuck shitters
    hasRole = False
    serverRoles = ctx.message.server.roles
    for e in ctx.message.author.roles:
        if e.name == "Admin":
            hasRole = True
    if hasRole and ctx.message.mentions:
        roleToRemove = get_role(serverRoles, 'Muted')
        memberToUnMute = ctx.message.server.get_member(ctx.message.mentions[0].id)
        try:
            rolesToAdd = dict_of_roles[memberToUnMute.id]
        except KeyError:
            return(await client.say("User isn't muted"))
        try:
            await client.remove_roles(memberToUnMute, roleToRemove)
        except discord.Forbidden:
            return(await client.say("I don't have permission to do that! <:monkaS:356891254006611970>"))
        await client.add_roles(memberToUnMute, *rolesToAdd)
        dict_of_roles.pop(memberToUnMute.id) #Removes member from the mute list
        return(await client.say("User {} is now unmuted".format(ctx.message.mentions[0])))
    elif hasRole and not ctx.message.mentions:
        return(await client.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
    else:
        return(await client.say("You don't have permission to use this command <:FeelsRageMan:356757133393657867>"))

def get_role(server_roles, target_name):
    for each in server_roles:
        if each.name == target_name:
            return each
    print("Didn't find role")
    return None

@client.command(pass_context=False)
async def twitter():
    

@client.command(pass_context=False)
async def about():
    return(await client.say("```markdown\nHello, I am Christopher. \nI am an administration bot made by Skykanin, written in Python using the discord.py API. If you want to look at my code \
    checkout my github repository [link](https://github.com/skykanin/Christopher-Bot).```"))

@client.command(pass_context=False)
async def commands():
    return(await client.say("For a full list of all my commands and how to use them, checkout my github repository (https://github.com/skykanin/Christopher-Bot) README file"))

@client.event
async def on_message(message):
    if message.content.lower() in list_of_strings:
        await client.add_reaction(message, "🐢")
        await client.add_reaction(message, "🚀")
    if message.content.lower() == "the power of js":
        await client.add_reaction(message, ":GODSTINY:366936804273815552")
    await client.process_commands(message)
        
client.run(config["token"])