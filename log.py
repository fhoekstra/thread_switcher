from datetime import datetime


def format_date_time(date_time: datetime):
    return date_time.strftime(r"%Y-%m-%d %H:%M:%S")


def log(message):
    print(message)
    with open('log.txt', 'a') as f:
        f.write(message + '\r\n')
