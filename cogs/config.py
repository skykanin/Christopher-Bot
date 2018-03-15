#!/usr/bin/python3
import discord
from discord.ext import commands
import json
import os
import sqlite3
from sqlite3 import OperationalError, IntegrityError

class Config:

    def __init__(self, discordClient):
        self.bot = discordClient
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.settings = ['guild_id', 'commands_disabled', 'roll_command_channel', 'admin_role']
        self.bot_owner_id = "128122507415781379"

        
        ''' conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("""CREATE TABLE settings (
                guild_id INTEGER PRIMARY KEY,
                commands_disabled BOOLEAN,
                roll_command_channel TEXT,
                admin_role TEXT
            )""") 
        conn.commit() '''

    async def on_server_join(self, server):
        # Set default values when entering new guild
        try:
            self.add_default_values(server)
        except IntegrityError as e:
            print("Guild_settings already exists for this guild. IntegrityError", e)
        except OperationalError as e:
            print("OperationalError", e)

        # Prints the guild settings for specific guild
        print(self.fetch_guild_settings(server))

    def add_default_values(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("INSERT INTO {} VALUES (?,?,?,?)".format(self.table), (server.id, False, server.default_channel.name, 'Admin',))
        conn.close()

    # Returns all the settings for a guild
    def fetch_guild_settings(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM {} WHERE guild_id=?".format(self.table), (server.id,))
            guild_settings = c.fetchone()
        conn.close()
        return guild_settings
    
    def check_for_admin_role(self, ctx):
        # Get admin role name for specific guild
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings[3], self.table), (ctx.message.server.id,))
            guild_role = c.fetchone()[0]
        conn.close()

        # Check if user has the guild admin role  
        for role in ctx.message.author.roles:
            if role.name == guild_role.title():
                return True
        return False

    # Checks if role or channel exists in guild
    def check_if_exists(self, target_name, list_name, check_type):
        # if we are checking channel
        if check_type == 'channel':         
            for element in list_name:
                print("target:",target_name, "channel:",element.name, "type:",str(element.type))
                if target_name == element.name and str(element.type) == 'text':
                    return True
            return False
        # if we are checking role
        elif check_type == 'role':
            for element in list_name:
                if target_name == element.name:
                    return True
            return False

    # Command for handling custom queries
    @commands.group(pass_context=True, invoke_without_command=True)
    async def query(self, ctx, *args):
        # TODO: Add custom queries
        #args = ' '.join(args)
        print(*args)
        if ctx.invoked_subcommand is None:
            return(await self.bot.say('Invalid subcommand for query passed...'))

    @query.command(pass_context=True)
    async def print_settings(self, ctx):
        # Check if user has permission to use this command
        if not self.check_for_admin_role(ctx):
            return(await self.bot.say("You don't have permission to use this command"))

        #Gets guild settings from database
        try:
            guild_settings = self.fetch_guild_settings(ctx.message.server)
        except Exception:
            return(await bot.say("Exception:", e))

        formated_guild_settings = ""

        for i in range(len(guild_settings)):
            formated_guild_settings += self.settings[i] + ": " + str(guild_settings[i]) + "\n"

        return(await self.bot.say("```sql\nSELECT * FROM '{0}'\n\n{1}```".format(self.table, formated_guild_settings)))

    @query.command(pass_context=True)
    async def switch_commands(self, ctx):
        # Check if user has permission to use this command
        if not self.check_for_admin_role(ctx):
            return(await self.bot.say("You don't have permission to use this command"))
            
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("SELECT commands_disabled FROM {} WHERE guild_id=?".format(self.table), (ctx.message.server.id,))
            except Exception:
                return(await bot.say("Exception:", e))

            commands_disabled = c.fetchone()[0]
        
        if commands_disabled:
            commands_disabled = False
        else:
            commands_disabled = True

        with conn:
            try:
                c.execute("UPDATE {} SET commands_disabled=? WHERE guild_id=?".format(self.table), (commands_disabled, ctx.message.server.id,))
                return(await self.bot.say("`commands_disabled` was switched to {}".format(commands_disabled)))
            except Exception:
                return(await bot.say("Exception:", e))
        conn.close()

    
    @query.command(pass_context=True)
    async def update_roll_channel(self, ctx, channel : str):
        if not self.check_for_admin_role(ctx):
            return(await self.bot.say("You don't have permission to use this command"))
        elif not self.check_if_exists(channel, ctx.message.server.channels, 'channel'):
            return(await self.bot.say("`{}` text channel doesn't exist in this server".format(channel)))
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("UPDATE {0} SET {1}=? WHERE {2}={3}".format(self.table, self.settings[2], self.settings[0], ctx.message.server.id), (channel,))
                return(await self.bot.say("`{0}` has been updated to `{1}`".format(self.settings[2], channel)))
            except Exception as e:
                return(await self.bot.say("Exception", e))
        conn.close()

    @query.command(pass_context=True)
    async def update_admin_role(self, ctx, role : str):
        if not self.check_for_admin_role(ctx):
            return(await self.bot.say("You don't have permission to use this command"))
        elif not self.check_if_exists(role, ctx.message.server.roles, 'role'):
            return(await self.bot.say("`{}` role doesn't exist in this server".format(role)))
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("UPDATE {0} SET {1}=? WHERE {2}={3}".format(self.table, self.settings[3], self.settings[0], ctx.message.server.id), (role,))
                return(await self.bot.say("`{0}` has been updated to `{1}`".format(self.settings[3], role)))
            except Exception as e:
                return(await self.bot.say("Exception", e))
        conn.close()

def setup(bot):
    bot.add_cog(Config(bot))