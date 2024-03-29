from operator import or_ as bitwise_or
from functools import reduce


class Core:
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

        if index is not None:
            self.index = index
            self.friendly_number = index + 1
        else:
            self.friendly_number: int = friendly_number
            self.index = friendly_number - 1

        self.total_num = total_num
        self.hyper_threading = hyper_threading

    def __repr__(self):
        return (f"Core {self._handle_padding()}"
                f"{self.friendly_number}/{self.total_num}")

    def _handle_padding(self) -> str:
        if self.total_num >= 10 and self.friendly_number < 10:
            return ' '
        return ''

    @property
    def thread_indices(self) -> tuple[int]:
        if not self.hyper_threading:
            return (self.index,)
        return (2*self.index, 2*self.index + 1)

    @property
    def affinity_mask(self):
        masks_per_thread = map(self._get_mask_from_thread, self.thread_indices)
        combined_mask = reduce(bitwise_or, masks_per_thread)
        return str(combined_mask)

    @classmethod
    def _get_mask_from_thread(cls, index):
        return cls._limit_for_32_bit(2 ** index)

    @staticmethod
    def _limit_for_32_bit(x: int) -> int:
        return x if x < 2 ** 31 else 2 ** 30


def get_cores(hyper_threading: bool, core_num: int) -> list[Core]:
    return [Core(core_num, index=n,
                 hyper_threading=hyper_threading)
            for n in range(core_num)]


def get_index_of_core_in(friendly_number: int, cores: list[Core]) -> int:
    try:
        [the_core] = (core
                      for core in cores
                      if core.friendly_number == friendly_number)
        return cores.index(the_core)
    except ValueError:
        raise ValueError("starting core number should be one of core numbers:"
                         f"{list(map(lambda x: x.friendly_number, cores))}")
