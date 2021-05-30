import os

import discord
from discord.ext import commands
import duckduckgo
import imgsearch


class Grabber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def grab(self, ctx, *, query: str = ""):
        """
        Command "!grab" followed by a description of the image. Bot find the image.
        :param ctx: Discord context
        :param query: A string describing the image
        :return: None
        """

        query = imgsearch.clean_query(query)
        if query == "":
            return await ctx.send(f'<@{ctx.author.id}>, No image to grab!')

        img_url = duckduckgo.search(query)
        if img_url == None:
            return await ctx.send(f'<@{ctx.author.id}>, No image found!')

        e = discord.Embed(color=discord.Color.purple(), title=query)
        e.set_image(url=img_url)
        await ctx.send(embed=e)

    @commands.command()
    async def invite(self, ctx):
        """
        Allows user to invite bot to their server
        :param ctx:
        :return:
        """
        await ctx.send(f'You can invite me with this link! \n{os.environ.get("INVITE")}')

    

def setup(bot):
    bot.add_cog(Grabber(bot))
