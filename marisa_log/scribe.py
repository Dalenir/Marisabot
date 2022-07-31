import logging

from colorama import Fore, Back, Style
import pathlib
from datetime import datetime

pathlib.Path('logs/').mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=f'logs/{datetime.today().date()}_witch.log', filemode='a')

witch_log = logging.getLogger('Marisa Mistakes')
witch_log.setLevel(logging.WARNING)
witch_log.addHandler(logging.FileHandler(filename=f"logs/witch_mistakes.log", mode='w'))


async def witch_error(error_text: str | Exception, file: pathlib.Path | None = None):
    text = f"\n[ERROR]\n[TIME] {datetime.today().time().strftime('%H:%M:%S')}\n[FILE] {file} " + '\n' +\
           '-------------------------------------------------\n' + f'{error_text}'
    print(Fore.RED + Back.BLACK + text + Style.RESET_ALL)
    witch_log.error(text)
