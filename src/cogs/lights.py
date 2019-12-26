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

class LightsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hue = HueController(bot)
        self.utils = Utils()
    
    async def cog_check(self, ctx):
        return await self.utils.checkOwner(ctx)
    
    @commands.group(
        invoke_without_command=True, name='lights', aliases=["light", "l"],
        description='Commands related to individual lights.'
    )
    async def lights(self, ctx):
        lights = await self.hue.getLights('name')

        embed = discord.Embed(title='💡 **Available Lights**')

        for name, value in lights.items():
            embed.add_field(name=f'**{name}**', value=f'🆔 {value.__dict__["light_id"]}', inline=False)
        
        await ctx.send(embed=embed)

    @lights.command(
        name='on',
        description='Turns a single light on.'
    )
    async def _light_on(self, ctx, name: str):
        res = await self.hue.turnLightOn(ctx, name)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Turned light {name} on successfully!**')

    @lights.command(
        name='off',
        description='Turns a single light off.'
    )
    async def _light_off(self, ctx, name: str):
        res = await self.hue.turnLightOff(ctx, name)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Turned light {name} off successfully!**')
    
    @lights.command(
        name='brightness',
        description='Changes a single light\'s brightness.'
    )
    async def _light_brightness(self, ctx, name: str, value: int):
        actualValue = (255/10) * value
        res = await self.hue.lightBrightness(ctx, name, actualValue)
        
        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Changed {name}\'s brightness to {value}!**')

    @lights.command(
        name='colour', aliases=['color'],
        description='Changes a single light\'s colour.'
    )
    async def _light_colour(self, ctx, name: str, x: float, y: float):
        if x > 1 or y > 1:
            await self.utils.sendEmbed(ctx, description=f'**The x and y coordinates cannot be greater than 1.**')
        else:
            colours = [x,y]
            res = await self.hue.lightColour(ctx, name, colours)

            if res:
                await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Changed {name}\'s colour to {colours}!**')

    @lights.command(
        name='random',
        description='Sets a single light\'s colour to a random one.'
    )
    async def _light_random(self, ctx, name: str):
        randomColour = [random.random(),random.random()]
        res = await self.hue.lightColour(ctx, name, randomColour)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Changed {name}\'s colour to a random colour!**')
    
    @lights.command(
        aliases=['info', 'status'], name='information',
        description='Shows the status of a single light.'
    )
    async def _light_information(self, ctx, name: str):
        res = await self.hue.lightStatus(ctx, name)

        if res:
            status = res["state"]

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.title = f'💡 **{name.capitalize()}**'

            embed.add_field(name='🔋 **Status**', value="{}".format("On" if status["on"] else "Off"), inline=False)
            embed.add_field(name='🔆 **Brightness**', value=f'{round((status["bri"]/255) * 10)}/10', inline=False)
            embed.add_field(name='🔦 **Hue**', value=status["hue"], inline=False)
            embed.add_field(name='🕯️ **Saturation**', value=status["sat"], inline=False)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LightsCog(bot))