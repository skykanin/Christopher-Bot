#!/usr/bin/python3
from discord.ext import commands
from twitch import TwitchClient
import calendar
import datetime
import discord
import json
import pytz
import random
import re
import twitter

class BotCommands:

    def __init__(self, discordClient, twitterApi, twitchClient):
        self.bot = discordClient
        self.api = twitterApi
        self.twitchClient = twitchClient
        self.muted_users = []
        self.month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}
        self.adminRoleName = "Admin"

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - ctx.message.timestamp
        return(await self.bot.say('Pong! Took {}ms'.format(delta.microseconds // 1000)))

    @commands.command(pass_context=True)
    async def mute(self, ctx): #fuck shitters
        toMute = ctx.message.content.split(' ')[0] == "!mute"

        hasAdminRole = False
        serverRoles = ctx.message.server.roles

        for e in ctx.message.author.roles:
            if e.name == self.adminRoleName:
                hasAdminRole = True
                break

        if not hasAdminRole:
            return(await self.bot.say("You don't have permission to use this command <:OverRustle:286162736625352716>"))
        
        if not ctx.message.mentions:
            if toMute:
                return(await self.bot.say("You haven't passed an argument. The command is: !mute <mentionUser>"))
            else:
                return(await self.bot.say("You haven't passed an argument. The command is: !unmute <mentionUser>"))
        else:
            mentionedMember = ctx.message.mentions[0]
            memberToToggleMute = ctx.message.server.get_member(mentionedMember.id)
            mutedRole = self.get_role(serverRoles, 'Muted')
            forbiddenMessage = "I don't have permission to do that! <:pepoS:350644750191165441>"
            failedMessage = "Failed to {} role! <:pepoS:350644750191165441>"
            returnMessage = "User {0} is now {1}"

            if toMute:
                if memberToToggleMute in self.muted_users:
                    return(await self.bot.say("{} already has the Muted role".format(mentionedMember)))
                try:
                    print("Roles to add", mutedRole)
                    await self.bot.add_roles(memberToToggleMute, mutedRole)
                    self.muted_users.append(memberToToggleMute.id)
                    print("Roles after addition", memberToToggleMute.roles)
                except discord.Forbidden:
                    return(await self.bot.say(forbiddenMessage))
                except discord.HTTPException:
                    return(await self.bot.say(failedMessage.format("add")))
                return(await self.bot.say(returnMessage.format(mentionedMember, "muted")))
            else:
                if memberToToggleMute not in self.muted_users:
                    return(await self.bot.say("{} does not have the Muted role".format(mentionedMember)))
                try:
                    print("Roles to remove", mutedRole)
                    await self.bot.remove_roles(memberToToggleMute, mutedRole)
                    print("Roles after removal", memberToToggleMute.roles)
                except discord.Forbidden:
                    return(await self.bot.say(forbiddenMessage))
                except discord.HTTPException:
                    return(await self.bot.say(failedMessage.format("remove")))
                return(await self.bot.say(returnMessage.format(mentionedMember, "unmuted")))
            

    @commands.command(pass_context=True)
    async def unmute(self, ctx): #uncuck shitters
        self.mute(ctx)

    def get_role(self, server_roles, target_name):
        return next((x for x in server_roles if x.name == target_name), None)

    @commands.command(pass_context=True)
    async def twitter(ctx, stebenTwitterId=4726147296, localTimeZone='Europe/Oslo'):
        tweetJSON = self.api.GetUserTimeline(user_id=stebenTwitterId, count=1, exclude_replies=True)[0]
        tweetObject = json.loads(str(tweetJSON))

        embed = discord.Embed(
            title = "Go to tweet",
            description = tweetObject["text"],
            url = "https://twitter.com/{0}/status/{1}".format(tweetObject["user"]["screen_name"], tweetObject["id_str"]),
            color = 0x00aced
        )
        embed.set_author(
            name = "{0} ({1})".format(tweetObject["user"]["screen_name"], tweetObject["user"]["name"]),
            url = "https://twitter.com/{}".format(tweetObject["user"]["screen_name"]),
            icon_url = tweetObject["user"]["profile_image_url"]
        )
        utcTime = buildDate(tweetObject["created_at"][4:].split(' '))
        localTime = utcTime.astimezone(pytz.timezone(localTimeZone)).strftime('%b %d, %Y' + ' at ' + '%H:%M' + ' Central European')
        embed.set_footer(text = localTime)
        return(await self.bot.send_message(ctx.message.channel, embed=embed))

    def buildDate(dateArray): #Example of dateArray: ["Oct", "18", "20:11:48", +0000, "2017"]
        seconds = int(dateArray[2][6:8])
        minutes = int(dateArray[2][3:5])
        hours = int(dateArray[2][0:2])
        day = int(dateArray[1])
        month = self.month_dict(dateArray[0])
        year = int(dateArray[4])
        return(datetime.datetime(year, month, day, hours, minutes, seconds, 0, tzinfo=pytz.UTC))

    @commands.command(pass_context=False)
    async def live(self, stebenChannelId="18074328", url="www.destiny.gg/bigscreen"):
        stream = self.twitchClient.streams.get_live_streams(channel=stebenChannelId, stream_type="live")
        channelName = self.twitchClient.channels.get_by_id(int(stebenChannelId)).name.capitalize()
        if stream:
            return(await self.bot.say("{0} {1} is live right now <:WhoahDude:309736750689943552>".format(url, channelName)))
        else:
            return(await self.bot.say("{0} is not live right now 😦".format(channelName)))

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        string = ctx.message.content
        maxVal = 100
    
        if string == '!roll':
            return(await self.bot.say("{}".format(random.randint(1,maxVal))))
        
        diceFaces = re.search('[dD]{1}\d{3}', string)

        if diceFaces == None:
            return(await self.bot.say("Incorrect use of command, dice faces not given"))

        diceFacesValue = int(diceFaces[1:]) #removes the d

        if diceFacesValue > 0 and diceFacesValue <= 100:
            return(await client.say("{}".format(random.randint(1,diceFacesValue))))

        return(await self.bot.say("Could not parse argument, number must be between 1 and 100. Example of correct use !roll d6"))

    @commands.command(pass_context=True)
    async def about(self, ctx):
        embed = discord.Embed(
            title = "I am Christopher Bot",
            description = "I am an administration bot made by Skykanin, \
            written in Python using the discord.py API. If you want to look \
            at my code checkout my github repository.",
            url = "https://github.com/skykanin/Christopher-Bot",
            color = 0xffffff
        )
        embed.set_author(
            name = "skykanin",
            url = "https://github.com/skykanin",
            icon_url = "https://i.imgur.com/vpCyIaM.png"
        )
        return(await self.bot.send_message(ctx.message.channel, embed=embed))
    
    
    @commands.command(pass_context=False)
    async def commands(self):
        return(await self.bot.say("For a full list of all my commands and how to use them, \
        checkout my github repository (https://github.com/skykanin/Christopher-Bot) README file"))