import os

import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.repolink = "https://github.com/ShamsAnsari/ImageBot"
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        description = f'[:robot: Invite me!]({os.environ.get("INVITE")})\n[:information_source: Github Repo]({self.repolink})'
        e = discord.Embed(color=discord.Color.purple(), title="Help Menu", description=description)
        e.add_field(name="*grab", value="Type \"*grab\" followed by a couple words to search for an image",
                    inline=False)
        e.add_field(name="*help", value="Type \"*help\" for the help menu", inline=False)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Misc(bot))
