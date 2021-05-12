from datetime import timedelta, datetime
import time


def wait_and_sync(waiting_period: timedelta,
                  sync: bool) -> None:
    if sync and waiting_period >= timedelta(minutes=1):
        waiting_period = adjust_wait_to_clock_minute(waiting_period)
    wait(waiting_period)


def adjust_wait_to_clock_minute(waiting_period: timedelta) -> timedelta:
    end_time = datetime.now() + waiting_period
    end_time = round_to_minutes(end_time)
    return end_time - datetime.now()


def round_to_minutes(end_time: datetime) -> datetime:
    round_up = bool(end_time.second > 30)
    rounded_minute = end_time.minute + 1 if round_up else end_time.minute
    return datetime(
        year=end_time.year,
        month=end_time.month,
        day=end_time.day,
        hour=end_time.hour,
        minute=rounded_minute,
        second=0, microsecond=0,
        tzinfo=end_time.tzinfo, fold=end_time.fold)


def wait(period: timedelta) -> None:
    time.sleep(period.total_seconds())
