import os

import discord
from discord.ext import commands



class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """
        Allows user to invite bot to their server
        :param ctx:
        :return:
        """
        await ctx.send(f'You can invite me with this link! \n{os.environ.get("INVITE")}')


def setup(bot):
    bot.add_cog(Misc(bot))
