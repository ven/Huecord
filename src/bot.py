import subprocess
import datetime
from time import time, sleep
from discord.ext import commands
import discord
from phue import Bridge, PhueRegistrationException
import random
import time
import sys, traceback
import asyncio


class Huecord(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            *args, **kwargs
        )

        self.check='✅'
        self.cross='❌'
        
        self.load_extension("jishaku")

        for extension in self.config.initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    @property
    def config(self):
        return __import__("config")

    def run(self):
        return super().run(self.config.token)

    async def on_ready(self):
        print(f'\n\nLogged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n')

        await self.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"the lights!"))
        print(f'Successfully logged in and booted...!')

    async def get_prefix(self, message):
        valid = [f"<@{self.user.id}> ",
                 f"<@!{self.user.id}> ",
                 f"<@{self.user.id}>",
                 f"<@!{self.user.id}>",
                 self.config.prefix]

        return valid

