import _thread
import datetime
import json
import os
import threading

import requests


class StatsLogger:
    def __init__(self, bot):
        self.num_servers = 0
        self.num_users = 0
        self.bot = bot
        self.stats_path = "logs/statslog.txt"
        self.bot_list_api_key = os.environ.get("DISCORD_BOT_LIST_API_KEY")
        self.id = os.environ.get("ID")

        self.log_stats()

        # update server stats every day
        threading.Timer(86400, self.log_stats).start()

    def send_stats(self):
        """
         Sends stats to discordbotslist.com
        :return:
        """
        url = f'https://api.discordbotslist.co/v1/public/bot/{self.id}/stats'
        h = {"authorization": self.bot_list_api_key, "content-type": "application/json"}
        b = json.dumps({"serverCount": self.num_servers}, separators=(',', ':'))
        re = requests.post(f"https://api.discordbotslist.co/v1/public/bot/{self.id}/stats", headers=h, data=b)
        print("Sent stats", re.text)

    def log_stats(self):
        """
        Logs stats to txt and also calls send_stats()
        :return:
        """
        self.num_servers = len(self.bot.guilds)
        self.num_users = len(self.bot.users)

        f = open(self.stats_path, "w")
        f.write(f'{datetime.datetime.now().strftime("Date: %m/%d/%Y  time: %H:%M:%S")}\n'
                f'Number of server: {self.num_servers}\nUsers: {self.num_users}')
        f.close()
        print("Logged stats ", datetime.datetime.now())

        self.send_stats()


class CommandLogger:
    def __init__(self, bot):
        self.bot = bot
        self.commandlogs_path = "logs/commandlogs.txt"

    def log_command_wrapper(self, ctx, return_image):
        _thread.start_new_thread(self.log_command, (ctx, return_image))

    def log_command(self, ctx, return_image):
        """
        Logs the "grab" command into a txt file everytime it is called
        :param ctx:
        :param return_image: url image of result of grab command

        :return:
        """
        dt_string = datetime.datetime.now().strftime("Date: %d/%m/%Y  time: %H:%M:%S")
        text = ctx.message.content
        user = ctx.author
        server = ctx.message.guild.name
        channel = ctx.message.channel

        f = open(self.commandlogs_path, "a")
        f.write(f'{dt_string}\n\tUser: {user}\n\tCommand: {text}\n\tImage: {return_image}'
                f'\n\tServer: {server}\n\tChannel: {channel}\n');
        f.close()

        print("Logged command ", datetime.datetime.now())
