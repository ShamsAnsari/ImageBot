import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

import logger

# load .env
load_dotenv()

# create bot
bot = commands.Bot(command_prefix="*", intents=discord.Intents.all(), case_insensitive=True, help_command=None)

# create logger

# list of extensions to load
extensions = ["grabber", "misc"]

# load extensions
count = 0
for ext in extensions:
    bot.load_extension(f"{ext}")
    print(f'Loaded {ext}')
    count += 1


# this event fires when the bot is "ready"
@bot.event
async def on_ready():
    await bot.wait_until_ready()

    # set activity status
    await bot.change_presence(activity=discord.Game('*help'))

    print('--------------------------')
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    print(f'Loaded {count} extensions')
    print('--------------------------')
    logger.StatsLogger(bot)


bot.run(os.environ.get('TOKEN'))
