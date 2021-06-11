import random
import re

import discord
from discord.ext import commands
import duckduckgo
import logger



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
        result_num = self.get_num(query)
        query = Grabber.clean_query(Grabber.clean_brackets(query))

        if query == "": return await self.send_error(ctx)

        img_url = duckduckgo.search(query, result_num)

        if img_url is None: return await self.send_error(ctx)

        e = discord.Embed(color=discord.Color.purple(), title=query)
        e.set_image(url=img_url)
        await ctx.send(embed=e)
        self.log.log_command_wrapper(ctx, img_url)

    @commands.command()
    async def grabpp(self, ctx, *, user: discord.User = None):
        """
        Grab's profile picture of person mentioned in message or author of message if no one is mentioned.
        :param ctx:
        :param user:
        :return:
        """
        if user is None:
            user = ctx.author
        image = user.avatar_url
        e = discord.Embed(color=discord.Color.purple(), title=f'{user.display_name}\'s Profile Picture')
        e.set_image(url=image)
        await ctx.send(embed=e)


    @staticmethod
    def get_num(msg):
        """
        Gets number inside < > brackets
        :param msg:
        :return:
        """
        if msg.find("<") >= 0 and msg.find(">") >= 0:
            num = msg[msg.find('<') + 1:msg.find('>')]
            if num.isdigit():
                return int(num)
        return 0

    @staticmethod
    async def send_error(ctx):
        """
        Sends an image of a funny cat if there is no image found.
        Codes are error codes on website
        :param ctx:
        :return:
        """
        codes = [100, 101, 102, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402,
                 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424,
                 425, 426, 429, 431, 444, 450, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599]
        await ctx.send(f'<@{ctx.author.id}>, No image to grab!')
        e = discord.Embed(color=discord.Color.purple())
        e.set_image(url=f'https://http.cat/{codes[random.randrange(0, len(codes))]}')
        return await ctx.send(embed=e)

    @staticmethod
    def clean_query(query):
        """
          Cleans the query, remove any troublesome characters
        """
        query = query.encode("ascii", "ignore").decode()
        query = re.sub(r'[^a-zA-Z0-9 ]', '', query).strip()
        return query

    @staticmethod
    def clean_brackets(msg):
        if msg.find("<") >= 0 and msg.find(">") >= 0:
            return (msg[:msg.find('<')] + msg[msg.find('>') + 1:]).strip()
        return msg


def setup(bot):
    bot.add_cog(Grabber(bot))
