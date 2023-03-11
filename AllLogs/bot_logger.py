import logging
import os
import pathlib
import socket
import sys
import traceback
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
        color_formatter = ColorFormatter(f"%(name)-10s %(levelname)-18s %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.infolog.addHandler(console)
        if os.getenv("PROD_LOGS"):
            sys.excepthook = BotLogger.exception_logging

    @staticmethod
    def exception_logging(exctype, value, tb):
        """
        Log exception by using the root logger.

        Parameters
        ----------
        exctype : type
        value : NameError
        tb : traceback
        """
        write_val = {'exception_type': str(exctype),
                     'message': str(traceback.format_tb(tb, 10))}
        logging.exception(str(write_val))


main_logger = BotLogger()
