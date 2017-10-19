import discord
from discord.ext import commands
import twitter
import json
import datetime
import pytz

config = json.loads(open("config.json", "r").read())

bot_description = "Admin bot"
bot_prefix = config["prefix"]

consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]

api = twitter.Api(consumer_key=consumerKey, consumer_secret=consumerSecret, access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
client = commands.Bot(description=bot_description, command_prefix=bot_prefix)

list_of_strings = ['best lang', 'what is the best programming language?', 'what language is the best?']
stebenId = 4726147296
dict_of_roles = {}
adminRoleName = "Admin"

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
        if e.name == adminRoleName:
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
        if e.name == adminRoleName:
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

@client.command(pass_context=True)
async def twitter(ctx):
    tweetObject = json.loads(str(api.GetUserTimeline(user_id=stebenId, count=1, exclude_replies=True)[0]))

    embed = discord.Embed(
        title = "Go to tweet",
        description = tweetObject["text"],
        url = "https://twitter.com/{0}/status/{1}".format(tweetObject["user"]["screen_name"], tweetObject["id_str"]),
        color = 0x00aced
    )
    embed.set_author(
        name = tweetObject["user"]["screen_name"] + " (" + tweetObject["user"]["name"] + ")",
        url = "https://twitter.com/" + tweetObject["user"]["screen_name"],
        icon_url = tweetObject["user"]["profile_image_url"]
    )
    utcTime = buildDate(tweetObject["created_at"][4:].split(' '))
    localTime = utcTime.astimezone(pytz.timezone('Europe/Oslo')).strftime('%b %d, %Y' + ' at ' + '%H:%M' + ' Central European')
    embed.set_footer(
       text = localTime
    )
    return(await client.send_message(ctx.message.channel, embed=embed))
    
def buildDate(dateArray): #["Oct", "18", "20:11:48", +0000, "2017"]
    seconds = int(dateArray[2][6:8])
    minutes = int(dateArray[2][3:5])
    hours = int(dateArray[2][0:2])
    day = int(dateArray[1])
    month = findMonthInt(dateArray[0])
    year = int(dateArray[4])
    return(datetime.datetime(year, month, day, hours, minutes, seconds, 0, tzinfo=pytz.UTC))

def findMonthInt(monthString):
    if(monthString == "Jan"):
        return(1)
    elif(monthString == "Feb"):
        return(2)
    elif(monthString == "Mar"):
        return(3)
    elif(monthString == "Apr"):
        return(4)
    elif(monthString == "May"):
        return(5)
    elif(monthString == "Jun"):
        return(6)
    elif(monthString == "Jul"):
        return(7)
    elif(monthString == "Aug"):
        return(8)
    elif(monthString == "Sep"):
        return(9)
    elif(monthString == "Oct"):
        return(10)
    elif(monthString == "Nov"):
        return(11)
    elif(monthString == "Dec"):
        return(12)
    else:
        return None

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