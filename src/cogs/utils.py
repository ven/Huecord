import discord
from discord.ext import commands
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'config')))
import config

class Utils():
    def __init__(self):
        self.config = config

    async def checkOwner(self, ctx):
        if not self.config.owner_only:
            return True
            
        if ctx.author.id == 204616460797083648:
            return True

        await self.sendEmbed(ctx, description='**Sorry, you do not have permission to use this command.**')
        return False

    async def sendEmbed(self, ctx, title: str=None, description: str=None):
        embed = discord.Embed(colour=discord.Colour.blue())

        embed.title = title
        embed.description = description

        return await ctx.send(embed=embed)