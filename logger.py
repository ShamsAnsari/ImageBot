import datetime
import threading
import _thread


class Logger:

    def __init__(self, bot):
        self.bot = bot
        self.commandlogs_path = "logs/commandlogs.txt"
        self.stats_path = "logs/statslog.txt"

        # update server stats every day
        threading.Timer(86400, self.log_stats).start()

    def log_command_wrapper(self, ctx, return_image):
        _thread.start_new_thread(self.log_command, (ctx, return_image))

    def log_command(self, ctx, return_image):
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

    def log_stats(self):
        f = open(self.stats_path, "w")
        f.write(f'{datetime.datetime.now().strftime("Date: %d/%m/%Y  time: %H:%M:%S")}\n'
                f'Number of server: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}')
        f.close()


        print("Logged stats ", datetime.datetime.now())
