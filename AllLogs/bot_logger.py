import logging
import pathlib
from datetime import datetime
from colorama import init, Fore, Back
from aiogram import loggers



class ColorFormatter(logging.Formatter):
    init(autoreset=True)
    COLORS = {
        "WARNING": Fore.RED,
        "ERROR": Fore.RED + Back.BLACK,
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "CRITICAL": Fore.RED + Back.BLACK
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + record.msg
        return logging.Formatter.format(self, record)


class BotLogger:
    infolog = None

    def __init__(self):
        today_for_log = datetime.now().strftime('%Y-%m-%d')
        pathlib.Path('AllLogs/bot_logs/').mkdir(parents=True, exist_ok=True)
        self.infolog = loggers.event

        self.infolog.setLevel(logging.INFO)

        self.infolog.addHandler(logging.FileHandler(filename=f"AllLogs/bot_logs/{today_for_log}.log", mode='a'))
        color_formatter = ColorFormatter("%(name)-10s %(levelname)-18s %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.infolog.addHandler(console)


main_logger = BotLogger()
