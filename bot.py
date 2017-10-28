import discord
from discord.ext import commands
import twitter
from twitch import TwitchClient
import json
import datetime
import pytz
import random
config = json.loads(open("config.json", "r").read())

bot_description = "Admin bot"
bot_prefix = config["prefix"]
consumerKey = config["consumer_key"]
consumerSecret = config["consumer_secret"]
accessTokenKey = config["access_token_key"]
accessTokenSecret = config["access_token_secret"]
clientId = config["twitch_client_id"]

#Bot, twitter, twitch
client = commands.Bot(description=bot_description, command_prefix=bot_prefix)
api = twitter.Api(consumer_key=consumerKey, consumer_secret=consumerSecret, access_token_key=accessTokenKey, access_token_secret=accessTokenSecret)
twitchClient = TwitchClient(client_id=clientId)

#message react
list_of_strings = ['best lang', 'what is the best programming language?', 'what language is the best?']
#twitter
stebenTwitterId = 4726147296
#Mute and unmute
dict_of_roles = {}
adminRoleName = "Admin"
#Combo counter
savedEmote = ""
counter = 0

@client.event
async def on_ready():
    print("Logged in")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print(discord.__version__)

@client.command(pass_context=True)
async def ping(ctx):
    now = datetime.datetime.utcnow()
    delta = now - ctx.message.timestamp
    return(await client.say('Pong! Took {}ms'.format(delta.microseconds // 1000)))

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
        rolesToSave = memberToMute.roles
        try:
            print("Roles to remove", memberToMute.roles)
            await client.remove_roles(memberToMute, *memberToMute.roles)
            print("Roles after removal", memberToMute.roles)
        except discord.Forbidden:
            return(await client.say("I don't have permission to do that! <:pepoS:350644750191165441>"))
        except discord.HTTPException:
            return(await client.say("Failed to remove roles! <:pepoS:350644750191165441>"))
        dict_of_roles[memberToMute.id] = rolesToSave #Adds member to the mute list
        print("Saved Original Roles", rolesToSave)
        await client.add_roles(memberToMute, rolesToAdd)
        print("Roles after adding mute role", memberToMute.roles)
        return(await client.say("User {} is now muted".format(ctx.message.mentions[0])))
    elif hasRole and not ctx.message.mentions:
        return(await client.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
    else:
        return(await client.say("You don't have permission to use this command <:OverRustle:286162736625352716>"))

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
            print("Roles to add", rolesToAdd)
        except KeyError:
            return(await client.say("User isn't muted"))
        try:
            await client.remove_roles(memberToUnMute, roleToRemove)
            print("Roles after removing mute role", memberToUnMute.roles)
        except discord.Forbidden:
            return(await client.say("I don't have permission to do that! <:pepoS:350644750191165441>"))
        await client.add_roles(memberToUnMute, *rolesToAdd)
        print("Roles after giving back original roles", memberToUnMute.roles)
        dict_of_roles.pop(memberToUnMute.id) #Removes member from the mute list
        return(await client.say("User {} is now unmuted".format(ctx.message.mentions[0])))
    elif hasRole and not ctx.message.mentions:
        return(await client.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
    else:
        return(await client.say("You don't have permission to use this command <:OverRustle:286162736625352716>"))

def get_role(server_roles, target_name):
    for each in server_roles:
        if each.name == target_name:
            return each
    print("Didn't find role")
    return None

@client.command(pass_context=True)
async def twitter(ctx):
    tweetObject = json.loads(str(api.GetUserTimeline(user_id=stebenTwitterId, count=1, exclude_replies=True)[0]))

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
async def live():
    stream = twitchClient.streams.get_live_streams(channel="18074328", stream_type="live")
    channelName = twitchClient.channels.get_by_id(18074328).name.capitalize()
    if stream:
        return(await client.say("{0} is live right now <:WhoahDude:309736750689943552>".format(channelName)))
    else:
        return(await client.say("{0} is not live right now 😦".format(channelName)))

valueList = {}

@client.command(pass_context=True)
async def values(ctx):
    global valueList
    if ctx.message.content in valueList:
        return(await client.say(valueList[ctx.message.content]))
    elif ctx.message.author.name in valueList:
        return(await client.say(valueList[ctx.message.author.name]))
    else:
        return(await client.say("Can't find data for user"))

@client.command(pass_context=True)
async def addValues(ctx):
    global valueList
    hasRole = False
    imgurLink = "https://imgur.com/"
    serverRoles = ctx.message.server.roles
    stringList = ctx.message.content.split(" ")

    for e in ctx.message.author.roles:
        if e.name == adminRoleName:
            hasRole = True

    if hasRole:
        if len(stringList) == 3 and imgurLink in stringList[2]:
            valueList[stringList[1]] = stringList[2]
            print(valueList)
            return(await client.say("8values result added"))
        elif len(stringList) == 2 and imgurLink in stringList[1]:
            valueList[ctx.message.author.name] = stringList[1]
            print(valueList)
            return(await client.say("8values result added"))
        else:
            return(await client.say("Incorrect use of command (name must not contain spaces) or imgur link not supplied"))
    else:
        return(await client.say("You do not have permission to use this command <:OverRustle:286162736625352716>"))

@client.command(pass_context=True)
async def roll(ctx):
    stringList = ctx.message.content.split(" ")
    maxVal = 100

    if len(stringList) > 1:
        del stringList[0]
    else:
        return(await client.say("{}".format(random.randint(1,100))))

    try:
        if int(stringList[0][1:]) <= maxVal and int(stringList[0][1:]) > 0 and stringList[0][0] == "d":
            return(await client.say("{}".format(random.randint(1,int(stringList[0][1:])))))
        elif stringList[0][0] != "d":
            return(await client.say("Missing delimiter 'd' in front of number"))
        else:
            return(await client.say("Number is over {0} or under 1".format(str(maxVal))))
    except ValueError:
        return(await client.say("Incorrect use of command, example of correct use !roll d6"))

@client.command(pass_context=True)
async def about(ctx):
    embed = discord.Embed(
        title = "I am Christopher Bot",
        description = "I am an administration bot made by Skykanin, written in Python using the discord.py API. If you want to look at my code checkout my github repository.",
        url = "https://github.com/skykanin/Christopher-Bot",
        color = 0xffffff
    )
    embed.set_author(
        name = "skykanin",
        url = "https://github.com/skykanin",
        icon_url = "https://i.imgur.com/vpCyIaM.png"
    )
    return(await client.send_message(ctx.message.channel, embed=embed))


@client.command(pass_context=False)
async def commands():
    return(await client.say("For a full list of all my commands and how to use them, checkout my github repository (https://github.com/skykanin/Christopher-Bot) README file"))

@client.event
async def on_message(message):
    global savedEmote
    global counter

    if message.content.lower() in list_of_strings:
        await client.add_reaction(message, "🐢")
        await client.add_reaction(message, "🚀")
    if "the power of js" in message.content.lower():
        await client.add_reaction(message, ":GODSTINY:347438305601912833")
    if "hot coco" in message.content.lower():
        await client.add_reaction(message, ":pepeComfy:372014257044193302")

    #comboCounter
    #print("Check content", message.content == savedEmote)
    #print("Check author", message.author.id == client.user.id)
    print(message.channel.name)
    if message.channel.name == "general":
        if message.author.id == client.user.id:
            #print("Ignore selfwritten messages")
            None
        elif message.content == savedEmote:
            counter+=1
            #print(counter)
        else:
            if counter > 1:
                await client.send_message(message.channel, savedEmote + " " + str(counter) + "x " + "c-c-c-combo") #print combo
            counter = 0 #reset counter
            savedEmote = '' #reset saved emote

            for emoji in message.server.emojis:
                if message.content == str(emoji):
                    savedEmote = str(emoji)
                    counter = 1                
            #print("savedEmote", savedEmote)
            #print("messageAuthor", message.author)   
    await client.process_commands(message)
        
client.run(config["token"])