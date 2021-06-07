import discord
from discord.ext import commands

import duckduckgo
import imgsearch
import logger
import random


class Grabber(commands.Cog):
    def __init__(self, bot):
        self.log = logger.CommandLogger(bot)
        self.bot = bot

    @commands.command()
    async def grab(self, ctx, *, query: str = ""):
        """
        Command "*grab" followed by a description of the image. Bot find the image.
        :param ctx: Discord context
        :param query: A string describing the image
        :return: None
        """

        query = imgsearch.clean_query(query)
        if query == "":
            return await self.send_error(ctx)

        img_url = duckduckgo.search(query)
        if img_url == None:
            return await self.send_error(ctx)

        e = discord.Embed(color=discord.Color.purple(), title=query)
        e.set_image(url=img_url)
        await ctx.send(embed=e)

        self.log.log_command_wrapper(ctx, img_url)

    async def send_error(self, ctx):
        codes = [100, 101, 102, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402,
                 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424,
                 425, 426, 429, 431, 444, 450, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599]
        await ctx.send(f'<@{ctx.author.id}>, No image to grab!')
        e = discord.Embed(color=discord.Color.purple())
        e.set_image(url=f'https://http.cat/{codes[random.randrange(0,len(codes))]}')
        return await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Grabber(bot))
