from pathlib import Path
from datetime import datetime

THIS_FILE = Path(__file__)
LOG_FILE = THIS_FILE.parent.parent / 'log.txt'


def format_date_time(date_time: datetime):
    return date_time.strftime(r"%Y-%m-%d %H:%M:%S")


def log(message):
    print(message)
    with open(LOG_FILE, 'a') as f:
        f.write(message + '\r\n')
