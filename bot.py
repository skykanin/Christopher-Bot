#!/usr/bin/python3
from discord.ext import commands
from discord.ext.commands import Bot
from twitch import TwitchClient
from botCommands import BotCommands
import calendar
import datetime
import discord
import json
import pymysql.cursors
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

sqlConnection = pymysql.connect(host=config["sql_host"], user=config["sql_user"], password=config["sql_password"], db=config["sql_db"], port=config["sql_port"], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

list_of_strings = ['best lang', 'what is the best programming language?', 'what language is the best?']
currentEmote = ""
counter = 0
combo_users=[]

@client.event
async def on_ready():
    print("Logged in")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print(discord.__version__)

@client.event
async def on_message(message):
    global list_of_strings
    global currentEmote
    global counter
    global combo_users

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

    #combo counter
    if message.channel.name == "general":
        if message.author.id == client.user.id:
            None
        elif currentEmote == '' and counter == 0:
            for emoji in message.server.emojis:
                if message.content == str(emoji):
                    currentEmote = str(emoji)
                    counter = 1
                    combo_users.append(message.author.id)
        elif message.content == currentEmote and message.author.id not in combo_users:
            counter+=1
        else:
            if counter > 1:
                await client.send_message(message.channel, currentEmote + " " + str(counter) + "x " + "c-c-c-combo") #print combo
            counter = 0 #reset self.counter
            currentEmote = '' #reset saved emote
            combo_users = [] #reset combo users list            
    await client.process_commands(message)

@client.event
async def on_server_join(server):
    try:
        with connection.cursor() as cursor:
            sql = "CREATE TABLE `{0}` (`userID` INT NOT NULL, `message` varchar(2000) NOT NULL, \
            `dateTime` DATETIME(6) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;".format(server.id)
            cursor.execute(sql)
        connection.commit()
    except:
        print("There is an error")

@client.event
async def on_error(event):
    client.connect(reconnect=True)

if __name__ == "__main__":
    client.run(config["token"])