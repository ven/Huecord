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


class GroupsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hue = HueController(bot)
        self.utils = Utils()
    
    async def cog_check(self, ctx):
        return await self.utils.checkOwner(ctx)

    @commands.group(
        invoke_without_command=True, name='groups', aliases=["group", "g"],
        description='Commands related to light groups.'
    )
    async def groups(self, ctx):
        groups = await self.hue.getGroups()

        embed = discord.Embed(title='💡 **Light Groups**')

        for id, info in groups.items():
            lightNames = [await self.hue.getLightName(ctx, int(x)) for x in info["lights"]]

            text = f"""
            🆔 **ID**: {id}
            🔦 **Lights:** {", ".join(lightNames)}
            ⚙️ **Type:** {info["type"]}
            🔋 **All On:** {info["state"]["all_on"]}
            """
            
            embed.add_field(name=f'**{info["name"]}**', value=text, inline=False)

        await ctx.send(embed=embed)

    @groups.command(
        name='on',
        description='Turns a light group on.'
    )
    async def _group_on(self, ctx, name: str):
        res = await self.hue.turnGroupOn(ctx, name)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Turned group {name.capitalize()} on successfully!**')

    @groups.command(
        name='off',
        description='Turns a light group off.'
    )
    async def _group_off(self, ctx, name: str):
        res = await self.hue.turnGroupOff(ctx, name)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Turned group {name.capitalize()} off successfully!**')
    
    @groups.command(
        name='brightness',
        description='Changes the brightness of a light group.'
    )
    async def _group_brightness(self, ctx, name: str, value: int):
        actualValue = (255/10) * value
        res = await self.hue.groupBrightness(ctx, name, actualValue)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Changed group {name}\'s brightness to {value}!**')

    @groups.command(
        name='delete',
        description='Deletes a light group.'
    )
    async def _group_delete(self, ctx, name: str):
        res = await self.hue.groupDelete(ctx, name)

        if res:
            await self.utils.sendEmbed(ctx, description=f'{self.bot.check} **Successfully deleted group {name}!**')

def setup(bot):
    bot.add_cog(GroupsCog(bot))
