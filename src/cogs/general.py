from phue import Bridge
from .hue import HueController
from .utils import Utils
import random
import time
import discord
from discord.ext import commands
import sys, traceback
import datetime
import asyncio

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hue = HueController(bot)
        self.utils = Utils()
    
    async def cog_check(self, ctx):
        return await self.utils.checkOwner(ctx)
    
    @commands.command(
        description='Attempts to connect with your Hue Bridge once the sync button has been pressed.'
    )
    async def connect(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = '⏳ **Attempting to connect...**'
        embed.description=f'Push the button in the middle of your Hue Bridge to establish a connection.'

        await ctx.send(embed=embed)

        await self.hue.connect()
    
    @commands.command(
        aliases=["configuration"],
        description='Returns your Hue Bridge configuration details.'
    )
    async def config(self, ctx):
        data = (await self.hue.getAPI())["config"]

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = '⚙️ **Hue Bridge Configuration**'
        
        embed.add_field(name='🌐 **IP Address**', value=data["ipaddress"], inline=False)
        embed.add_field(name='📡 **Zigbee Channel**', value=data["zigbeechannel"], inline=False)
        embed.add_field(name='📫 **API Version**', value=data["apiversion"], inline=False)
        embed.add_field(name='📝 **Model ID**', value=data["modelid"], inline=False)
        embed.add_field(name='🕒 **Timezone**', value=data["timezone"], inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GeneralCog(bot))