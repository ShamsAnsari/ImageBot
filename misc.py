import os
import random
from pathlib import Path

import discord
from discord.ext import commands

import photomosaic


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
        # grabpp
        e.add_field(name="*grabpp", value="Type \"*grabpp\" and @ (mention) someone to get their profile picture.")
        # help command
        e.add_field(name="*help", value="Type \"*help\" for the help menu", inline=False)
        e.add_field(name="*photomosaic", value="Type \"*photomosaic\" and @ (mention) someone to craete a photomosaic of their profile picture.", inline=False)
        e.set_image(url="https://media.giphy.com/media/Lt5eOpMHfyHveYg8Bu/giphy.gif")
        e.set_footer(text="Email shamsahmedansari@gmail.com for bugs.")
        await ctx.send(embed=e)

    @commands.command()
    async def photomosaic(self, ctx, user: discord.User = None):

        if user is None and not bool(ctx.guild.icon_url):
            print("jumble: No icon found")
            return
        if user is None:
            print("No @")
            image_url = ctx.guild.icon_url

        await ctx.send('This may take a while, please wait.')
        # save icon
        image_url = user.avatar_url  # str(ctx.guild.icon_url)
        dir = os.path.join(os.getcwd(), 'mosaic', str(ctx.guild.id))
        Path(dir).mkdir(parents=True, exist_ok=True)
        image_path = os.path.join(dir, 'icon.png')
        await image_url.save(image_path)

        # save images
        dir_avatars = os.path.join(dir, 'avatars')
        Path(dir_avatars).mkdir(parents=True, exist_ok=True)
        for member in ctx.guild.members:
            await member.avatar_url.save(os.path.join(dir_avatars, f'{member.id}.png'))
        output_path = photomosaic.create_mosaic(dir, image_path, dir_avatars)
        print(output_path)
        output_img = discord.File(output_path)
        await ctx.send(
            'This is a mosaic of your icon created with the profile pictures of the people in this server. '
            'ZOOM in to see each individual Profile picture')

        await ctx.send(file=output_img)
        print("Jumbled")


def setup(bot):
    bot.add_cog(Misc(bot))
