import datetime
import threading
import _thread

class Logger:

    def __init__(self, bot):
        self.bot = bot
        self.commandlogs_path = "logs/commandlogs.txt"
        self.stats_path = "logs/statslog.txt"

        threading.Timer(30, self.log_stats).start()

    def log_command_wrapper(self, command, user, time, return_image):
        _thread.start_new_thread(self.log_command, (command, user, time, return_image))

    def log_command(self, command, user, time, return_image):
        f = open(self.commandlogs_path, "a")
        dt_string = time.strftime("Date: %d/%m/%Y  time: %H:%M:%S")
        f.write(f'{dt_string}\n\tUser: {user}\n\tCommand: {command}\n\tImage: {return_image}\n');
        f.close()

        print("Logged command ", datetime.datetime.now())

    def log_stats(self):
        f = open(self.stats_path, "w")
        f.write(f'{datetime.datetime.now().strftime("Date: %d/%m/%Y  time: %H:%M:%S")}\n'
                f'Number of server: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}')
        f.close()

        print("Logged stats ", datetime.datetime.now())