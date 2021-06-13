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

        # grab command
        e.add_field(name="*grab",
                    value="Type \\*grab <optional num> followed by a couple words to search for an image.",
                    inline=False)
        # photomosaic
        e.add_field(name="*photomosaic", value="Type \"*photomosaic\" and @ (mention) someone to craete a photomosaic of their profile picture. (Still in beta)", inline=False)

        # grabpp
        e.add_field(name="*grabpp", value="Type \"*grabpp\" and @ (mention) someone to get their profile picture.")
        # info
        e.add_field(name="*stats", value="Type \"*info\" for the bot stats", inline=False)
        # help command
        e.add_field(name="*help", value="Type \"*help\" for the help menu", inline=False)
        e.set_image(url="https://media.giphy.com/media/Lt5eOpMHfyHveYg8Bu/giphy.gif")
        e.set_footer(text="Email shamsahmedansari@gmail.com for bugs.")
        await ctx.send(embed=e)

    @commands.command()
    async def stats(self, ctx):
        await ctx.send(f'Number of server: {len(self.bot.guilds)}\n Number of people: {len(self.bot.users)}')


def setup(bot):
    bot.add_cog(Misc(bot))
