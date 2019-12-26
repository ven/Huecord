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


class ScenesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_check(self, ctx):
        return await self.bot.utils.checkOwner(ctx)

    @commands.group(
        invoke_without_command=True, aliases=["s", "scene"],
        description='Commands related to light scenes.'
    )
    async def scenes(self, ctx):
        scenes = await self.bot.hue.getScenes()

        embed = discord.Embed(title='💡 **Light Scenes**')

        for id, info in scenes.items():
            lightNames = [await self.bot.hue.getLightName(ctx, int(x)) for x in info["lights"]]

            text = f"""
            🔦 **Lights:** {", ".join(lightNames)}
            ⚙️ **Type:** {info["type"]}
            """
            
            embed.add_field(name=f'**{info["name"]}**', value=text, inline=False)

        await ctx.send(embed=embed)
    
    @scenes.command(
        name='run',
        description='Enables a light scene.'
    )
    async def _run(self, ctx, groupName: str, *, sceneName: str):
        res = await self.bot.hue.runScene(groupName=groupName, sceneName=sceneName)

        if res:
            await self.bot.utils.sendEmbed(ctx, description=f'{self.bot.check} **Successfully ran scene `{sceneName}` in group `{groupName}`!**')

def setup(bot):
    bot.add_cog(ScenesCog(bot))
