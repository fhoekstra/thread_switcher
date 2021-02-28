from subprocess import run
import time
from datetime import datetime as dt
from datetime import timedelta
from typing import Iterable

from core import Core, get_cores


def main(cfg: dict):

    cores = get_cores(cfg["hyper_threading"], cfg["core_num"])

    try:
        for thread in get_infinite_iterator(cores):
            log_starting_core(thread)
            set_active_core_for(thread, cfg["process_to_switch"])
            wait_and_sync(cfg["switch_every"], cfg["sync_on_clock_minute"])
    except KeyboardInterrupt as e:
        print("Stopped")
        raise(e)
        quit()


def log_starting_core(core: Core):
    message = dt.now().strftime(r"%Y-%m-%d %H:%M:%S") + f" switching to {core}"
    print(message)
    with open('log.txt', 'a') as f:
        f.write(message + '\r\n')


def get_infinite_iterator(collection: list[Core]) -> Iterable[Core]:
    length = len(collection)
    i = 0
    while True:
        if i >= length:
            i = 0
        yield collection[i]
        i += 1


def set_active_core_for(core: Core, process_name: str) -> None:
    run('Powershell "ForEach($PROCESS in'
        + f' GET-PROCESS {process_name})'
        + ' { $PROCESS.ProcessorAffinity=' + core.affinity_mask
        + '}"')


def wait_and_sync(waiting_period: timedelta,
                  sync: bool) -> None:
    if sync and waiting_period >= timedelta(minutes=1):
        waiting_period = adjust_wait_to_clock_minute(waiting_period)
    wait(waiting_period)


def adjust_wait_to_clock_minute(waiting_period: timedelta) -> timedelta:
    end_time = dt.now() + waiting_period
    end_time = _round_to_minutes(end_time)
    return end_time - dt.now()


def _round_to_minutes(end_time: dt) -> dt:
    round_up = bool(end_time.second > 30)
    return dt(end_time.year, end_time.month, end_time.day,
              hour=end_time.hour,
              minute=end_time.minute + 1 if round_up else end_time.minute,
              second=0, microsecond=0,
              tzinfo=end_time.tzinfo, fold=end_time.fold)


def wait(period: timedelta) -> None:
    time.sleep(period.total_seconds())


if __name__ == '__main__':
    from settings import cfg
    main(cfg)
