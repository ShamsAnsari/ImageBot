import discord
from discord.ext import commands
import imgsearch
"""
Group 3 project
@author Shams Ansari, Kenny (Kyungryun) Kim
add you name here if you're in this project
"""


class Grabber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def grab(self, ctx, *, query: str = ""):
        """
        Displays the first image found when searching for query on the bing browser
        :param ctx: Discord context
        :param query: A string describing the image
        :return: None
        """

        query = imgsearch.clean_query(query)
        if query == "":
            return await ctx.send(f'<@{ctx.author.id}>, No image to grab!')

        img_url = imgsearch.ImageSearch().image_search(query)
        e = discord.Embed(color=discord.Color.teal(), title=query)
        e.set_image(url=img_url)
        await ctx.send(embed=e)



def setup(bot):
    bot.add_cog(Grabber(bot))
