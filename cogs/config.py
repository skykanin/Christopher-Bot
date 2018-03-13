#!/usr/bin/python3
import discord
from discord.ext import commands
import json
import os
import sqlite3
from sqlite3 import OperationalError

class Config:

    def __init__(self, discordClient):
        self.bot = discordClient
        self.db = 'guild_settings.db'
        self.table = 'settings'

        
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
        #set default values when entering new guild
        try:
            self.add_default_values(server)
        except OperationalError as e:
            print("OperationalError", e)

        #prints the guild settings for specific guild
        print(self.fetch_guild_settings(server))

    def add_default_values(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("INSERT INTO {} VALUES (?,?,?,?)".format(self.table), (server.id, False, 'general', 'Admin',))
        conn.commit()
        conn.close()

    def fetch_guild_settings(self, server):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT * FROM {} WHERE guild_id=?".format(self.table), (server.id,))
        guild_settings = c.fetchone()
        conn.commit()
        conn.close()
        return guild_settings

    @commands.command(pass_context=True)    
    def config_commands(self, ctx):
        # TODO: implement command to toggle command_disabled setting
    
    @commands.command(pass_context=True)    
    def config_roll_channel(self, ctx):
        # TODO: implement command to toggle roll_command_channel setting

    @commands.command(pass_context=True)    
    def config_admin_role(self, ctx):
        # TODO: implement command to toggle admin_role setting


def setup(bot):
    bot.add_cog(Config(bot))