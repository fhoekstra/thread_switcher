from subprocess import run
import time
from datetime import datetime as dt
from datetime import timedelta
from typing import Iterable, Optional


cfg = {
    ##########################################################################
    "process_to_switch": "prime95",
    # name of process (e.g. "cinebench")
    "core_num": 6,
    # number of cores
    "switch_every": timedelta(minutes=5),
    # time between switching threads
    "sync_to": timedelta(minutes=1),
    # synchronize with wall time or put None for no synchronization
    "load_every_thread_separately": False,
    # legacy behavior TODO implement new behavior
    "hyper_threading": True,
    # whether your CPU has 2 threads per core
    ##########################################################################
}


class Thread:
    def __init__(self, total_num: int,
                 index: int = None, friendly_number: int = None,
                 hyper_threading: bool = True):
        """
        total_num is total number of threads.
        index is zero-indexed thread index
        friendly_number is 1-indexed thread index
        """
        if index is None and friendly_number is None:
            raise ValueError("One of index, friendly_number must be"
                             " provided as an int")
        if ((index is not None) and (friendly_number is not None)
                and (friendly_number != index + 1)):
            raise ValueError("index must be 1 lower than friendly_number")

        self.total_num = total_num

        if index is not None:
            self.index = index
            self.friendly_number = index + 1
        else:
            self.friendly_number = friendly_number
            self.index = friendly_number - 1

        if hyper_threading:
            assert self.total_num % 2 == 0
            self.core_index = int(self.index / 2)
            self.core_friendly_number = self.core_index + 1
            self.core_total = int(self.total_num / 2)
        else:
            self.core_index, self.core_friendly_number, self.core_total = \
                self.index, self.friendly_number, self.total_num

    def __repr__(self):
        return (f"Thread {self.friendly_number}/{self.total_num}  "
                f"{' ' if self.friendly_number < 10 else ''}"  # padding
                f"Core {self.core_friendly_number}/{self.core_total}")

    @property
    def affinity_mask(self):
        return str(2**self.index) if self.index < 31 else str(2**30)


def log_starting_thread(thread: Thread):
    message = f"{dt.now()} switching to {thread}"
    print(message)
    with open('log.txt', 'a') as f:
        f.write(message + '\r\n')


def get_infinite_iterator(collection: list[Thread]) -> Iterable[Thread]:
    length = len(collection)
    i = 0
    while True:
        if i >= length:
            i = 0
        yield collection[i]
        i += 1


def main(cfg: dict):
    threads = get_threads(cfg["hyper_threading"], cfg["core_num"])

    try:
        for thread in get_infinite_iterator(threads):
            log_starting_thread(thread)
            set_active_core_for(thread, cfg["process_to_switch"])
            wait_and_sync(cfg["switch_every"], cfg["sync_to"])
    except KeyboardInterrupt as e:
        print("Stopped")
        raise(e)
        quit()


def get_threads(hyper_threading: bool, core_num: int) -> list[Thread]:
    thread_num = (int(hyper_threading) + 1) * core_num
    return [Thread(thread_num, index=n,
                   hyper_threading=hyper_threading)
            for n in range(thread_num)]


def set_active_core_for(thread: Thread, process_name: str) -> None:
    run('Powershell "ForEach($PROCESS in'
        + f' GET-PROCESS {process_name})'
        + ' { $PROCESS.ProcessorAffinity=' + thread.affinity_mask
        + '}"')


def wait_and_sync(waiting_period: timedelta,
                  sync: Optional[timedelta]) -> None:
    if sync is not None:
        wait_for_sync(sync)
    wait(waiting_period)


def wait_for_sync(sync: timedelta) -> None:
    pass
    # TODO implement this


def wait(period: timedelta) -> None:
    time.sleep(period.total_seconds())


if __name__ == '__main__':
    main(cfg)
