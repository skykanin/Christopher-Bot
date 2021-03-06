#!/usr/local/bin/python3
import discord
from discord.ext import commands
import json
import os
import sqlite3
from sqlite3 import OperationalError, IntegrityError

class Config(commands.Cog):

    def __init__(self, discordClient):
        self.bot = discordClient
        self.db = 'guild_settings.db'
        self.table = 'settings'
        self.bot_owner_id = "128122507415781379"
        self.settings = {'guild_id': 'guild_id',
                        'guild_name': 'guild_name',
                        'commands_disabled': 'commands_disabled',
                        'roll_channel': 'roll_channel',
                        'osu_channel': 'osu_channel',
                        'admin_role': 'admin_role'}

        
        ''' conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE settings (
                    guild_id INTEGER PRIMARY KEY,
                    guild_name TEXT,
                    commands_disabled BOOLEAN,
                    roll_channel TEXT,
                    osu_channel TEXT,
                    admin_role TEXT
                )""") 
        conn.close() '''

        """ conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("DROP TABLE {}".format(self.table))
            except Exception as e:
                print(e)
        conn.close()
        print("Deleted table") """

    async def on_guild_join(self, guild):
        # Set default values when entering new guild
        try:
            self.add_default_values(guild)
        except IntegrityError as e:
            print("Guild_settings already exists for this guild. IntegrityError", e)
        except OperationalError as e:
            print("OperationalError", e)

        # Prints the guild settings for specific guild
        print(self.fetch_guild_settings(guild))

    def add_default_values(self, guild):
        # Choose the first text channel as default channel
        for channel in guild.text_channels:
            defualt = channel.name
            break

        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("INSERT INTO {} VALUES (?,?,?,?,?,?)".format(self.table),
            (guild.id, guild.name, False, defualt, defualt, 'Admin',))
        conn.close()

    # Returns all the settings for a guild
    def fetch_guild_settings(self, guild):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM {} WHERE guild_id=?".format(self.table), (guild.id,))
            guild_settings = c.fetchone()

            c.execute('PRAGMA TABLE_INFO({})'.format(self.table))
            names = [tup[1] for tup in c.fetchall()]
        conn.close()

        for i in range(len(names)):
            names[i] = str(names[i]) + ": " + str(guild_settings[i])

        return names
    
    def check_for_admin_role(self, ctx):
        # Get admin role name for specific guild
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            c.execute("SELECT {} FROM {} WHERE guild_id=?".format(self.settings['admin_role'], self.table), (ctx.message.guild.id,))
            guild_role = c.fetchone()[0]
        conn.close()

        # Check if user has the guild admin role  
        for role in ctx.message.author.roles:
            if role.name == guild_role.title():
                return True
        return False

    # Checks if role or channel exists in guild
    def check_if_exists(self, target_name, list_name):
        for element in list_name:
            if target_name == element.name:
                return True
        return False

    # Command for handling custom queries
    @commands.group(invoke_without_command=True)
    async def query(self, ctx, *args):
        if ctx.invoked_subcommand is None and args == "":
            return(await ctx.send('Invalid subcommand for query passed...'))

        if args[0] == 'select' or args[0] == "select".upper():
            query_type = 'get'
        else:
            query_type = 'set'

        query = ' '.join(args)
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        if query_type == 'get':
            with conn:
                try:
                    c.execute(query)
                    get = c.fetchall()
                    return(await ctx.send(get))
                except Exception as e:
                    return(await ctx.send(e))
        else:
            with conn:
                try:
                    c.execute(query)
                    return(await ctx.send("Query executed"))
                except Exception as e:
                    return(await ctx.send(e))

    @query.command()
    async def print_settings(self, ctx):
        # Check if user has permission to use this command
        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command"))

        # Gets guild settings from database
        try:
            guild_settings = self.fetch_guild_settings(ctx.message.guild)
        except Exception as e:
            return(await ctx.send("Exception:", e))

        formated_guild_settings = ""

        for element in guild_settings:
            formated_guild_settings += element + "\n"

        return(await ctx.send("```sql\nSELECT * FROM '{0}' WHERE guild_id={1};\n\n{2}```".format(self.table, guild_settings[0][10:], formated_guild_settings)))

    @query.command()
    async def switch_commands(self, ctx):
        # Check if user has permission to use this command
        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command"))
            
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("SELECT commands_disabled FROM {} WHERE guild_id=?".format(self.table), (ctx.message.guild.id,))
            except Exception as e:
                return(await ctx.send("Exception:", e))

            commands_disabled = c.fetchone()[0]
        
        if commands_disabled:
            commands_disabled = False
        else:
            commands_disabled = True

        with conn:
            try:
                c.execute("UPDATE {} SET commands_disabled=? WHERE guild_id=?".format(self.table), (commands_disabled, ctx.message.guild.id,))
                return(await ctx.send("`commands_disabled` was switched to {}".format(commands_disabled)))
            except Exception as e:
                return(await ctx.send("Exception:", e))
        conn.close()

    
    @query.command()
    async def update_roll_channel(self, ctx, channel : str):
        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command"))
        elif not self.check_if_exists(channel, ctx.message.guild.text_channels):
            return(await ctx.send("`{}` text channel doesn't exist in this guild".format(channel)))
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("UPDATE {0} SET {1}=? WHERE {2}={3}".format(self.table, self.settings['roll_channel'], self.settings['guild_id'], ctx.message.guild.id), (channel,))
                return(await ctx.send("`{0}` has been updated to `{1}`".format(self.settings['roll_channel'], channel)))
            except Exception as e:
                return(await ctx.send("Exception", e))
        conn.close()

    @query.command()
    async def update_osu_channel(self, ctx, channel : str):
        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command"))
        elif not self.check_if_exists(channel, ctx.message.guild.text_channels):
            return(await ctx.send("`{}` text channel doesn't exist in this guild".format(channel)))
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("UPDATE {0} SET {1}=? WHERE {2}={3}".format(self.table, self.settings['osu_channel'], self.settings['guild_id'], ctx.message.guild.id), (channel,))
                return(await ctx.send("`{0}` has been updated to `{1}`".format(self.settings['osu_channel'], channel)))
            except Exception as e:
                return(await ctx.send("Exception", e))
        conn.close()

    @query.command()
    async def update_admin_role(self, ctx, role : str):
        if not self.check_for_admin_role(ctx):
            return(await ctx.send("You don't have permission to use this command"))
        elif not self.check_if_exists(role, ctx.message.guild.roles):
            return(await ctx.send("`{}` role doesn't exist in this guild".format(role)))
        
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        with conn:
            try:
                c.execute("UPDATE {0} SET {1}=? WHERE {2}={3}".format(self.table, self.settings['admin_role'], self.settings['guild_id'], ctx.message.guild.id), (role,))
                return(await ctx.send("`{0}` has been updated to `{1}`".format(self.settings['admin_role'], role)))
            except Exception as e:
                return(await ctx.send("Exception", e))
        conn.close()

def setup(bot):
    bot.add_cog(Config(bot))
