from subprocess import run
from datetime import datetime as dt
from typing import Iterable

from core import Core, get_cores
from log import format_date_time, log
from timing import wait_and_sync


def main(cfg: dict):

    cores = get_cores(cfg["hyper_threading"], cfg["core_num"])

    try:
        for core in get_infinite_core_iterator(cores, cfg["starting_core"]):
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


def get_infinite_core_iterator(cores: list[Core],
                               starting_core_friendly_number: int) \
        -> Iterable[Core]:
    starting_index = get_index_of_core_in(starting_core_friendly_number, cores)
    return get_infinite_iterator(cores, starting_index)


def get_index_of_core_in(friendly_number: int, cores: list[Core]) -> int:
    try:
        the_core = get_the_core_with(friendly_number, cores)
        return cores.index(the_core)
    except StopIteration:
        raise ValueError("starting core number should be one of core numbers:"
                         f"{list(map(lambda x: x.friendly_number, cores))}")


def get_the_core_with(friendly_number: int, cores: list[Core]) -> Core:

    def is_core_with_number(core: Core):
        return core.friendly_number == friendly_number

    return next(filter(is_core_with_number, cores))


def get_infinite_iterator(collection: list,
                          starting_index: int) \
        -> Iterable:
    length = len(collection)
    i = starting_index
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
