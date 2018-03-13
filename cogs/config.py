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
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format('admin_role', self.table), (ctx.message.server.id,))
            guild_role = c.fetchone()
        conn.close()

        # Check if user has the guild admin role  
        for role in ctx.message.author.roles:
            if role.name in guild_role:
                return True
        return False

    # Checks if role exists in guild
    def check_role_exists(self, role_name, server_roles):
        if role_name in server_roles:
            return True
        else:
            return False

    # Command for handling custom queries
    @commands.group(pass_context=True)
    async def query(self, ctx):
        # TODO: Add custom queries
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
            except Exception:
                return(await bot.say("Exception:", e))
        conn.close()

        return(await self.bot.say("`commands_disabled` was switched to {}".format(commands_disabled)))
    
    @query.command(pass_context=True)
    async def update_roll_channel(self, ctx):
        # TODO: implement command to toggle roll_command_channel setting
        if not self.check_for_admin_role(ctx):
            return(await self.bot.say("You don't have permission to use this command"))
        elif not self.check_role_exists(ctx.message.content, ctx.message.server.roles):
            return(await self.bot.say("This role doesn't exist in this server"))

    @query.command(pass_context=True)
    async def update_admin_role(self, ctx):
        # TODO: implement command to toggle admin_role setting
        print("Nothing here yet")


def setup(bot):
    bot.add_cog(Config(bot))