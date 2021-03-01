from subprocess import run
from datetime import datetime as dt
from typing import Iterable

from core import Core, get_cores
from log import format_date_time, log
from timing import wait_and_sync


def main(cfg: dict):

    cores = get_cores(cfg["hyper_threading"], cfg["core_num"])

    try:
        for core in get_infinite_iterator(cores):
            log_starting_core(core)
            set_active_core_for(core, cfg["process_to_switch"])
            wait_and_sync(cfg["switch_every"], cfg["sync_on_clock_minute"])
    except KeyboardInterrupt as e:
        print("Stopped")
        raise(e)
        quit()


def log_starting_core(core: Core):
    message = format_date_time(dt.now()) + f" switching to {core}"
    log(message)


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


if __name__ == '__main__':
    from settings import cfg
    main(cfg)
