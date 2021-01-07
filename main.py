from subprocess import run
import time
from datetime import datetime as dt


cfg = {
    ##########################################################################
    "process_to_switch": "prime95",  # name of process (e.g. "cinebench")    #
    "core_num": 6,  # number of cores                                        #
    "sec_between_switch": 5,  # number of seconds between switching threads  #
    "hyper_threading": True,    # whether your CPU has hyperthreading        #
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
        return str(2**self.index) if self.index < 32 else str(2**31)


def log_starting_thread(thread: Thread):
    message = f"{dt.now()} switching to {thread}"
    print(message)
    with open('log.txt', 'a') as f:
        f.write(message + '\r\n')


def get_infinite_iterator(collection: list):
    length = len(collection)
    i = 0
    while True:
        if i >= length:
            i = 0
        yield collection[i]
        i += 1


def main(cfg: dict):
    thread_num = (cfg["hyper_threading"] + 1) * cfg["core_num"]
    thread_list = [Thread(thread_num, index=n,
                          hyper_threading=cfg["hyper_threading"])
                   for n in range(thread_num)]

    try:
        for thread in get_infinite_iterator(thread_list):
            log_starting_thread(thread)
            run('Powershell "ForEach($PROCESS in'
                + f' GET-PROCESS {cfg["process_to_switch"]})'
                + ' { $PROCESS.ProcessorAffinity=' + thread.affinity_mask
                + '}"')
            time.sleep(cfg["sec_between_switch"])
    except KeyboardInterrupt as e:
        print("Stopped")
        raise(e)
        quit()


if __name__ == '__main__':
    main(cfg)
