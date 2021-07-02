from math import trunc
from size import size
from access import DiskAccess
import random
from math import trunc

def repeatGenerator(rep):
    yield rep


class Workload:
    """Base workload class, generator of DiskAccess"""

    def __init__(self) -> None:
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError


class CustomWorkload(Workload):
    """
    CustomWorkload: a generator of `DiskAccess` class
            The workload depends on multiple generators to generate the 
            size, position and R/W of each access, and all of them can be
            overriden by a combined generator that provides all of the
            three elements each time
    """

    def __init__(self, length_gen=None, pos_gen=None, mode_gen=None, all_gen=None):
        super().__init__()
        # generators for access size, location, r/w
        self.length_gen = length_gen
        self.pos_gen = pos_gen
        self.mode_gen = mode_gen
        # generators for combined distribution
        # return a dictionary of {"size", "loc", "mode"}
        self.all_gen = all_gen

    def set_length_gen(self, length_gen):
        self.length_gen = length_gen
        self.all_gen = None

    def set_pos_gen(self, pos_gen):
        self.pos_gen = pos_gen
        self.all_gen = None

    def set_rw_gen(self, mode_gen):
        self.mode_gen = mode_gen
        self.all_gen = None

    def set_all_gen(self, all_gen):
        self.all_gen = all_gen
        self.length_gen = None
        self.pos_gen = None
        self.mode_gen = None

    def __next__(self):
        if self.all_gen:
            next_access = next(self.all_gen)
            return DiskAccess(**next_access)
        elif self.pos_gen and self.length_gen and self.mode_gen:
            next_length = next(self.length_gen)
            next_pos = next(self.pos_gen)
            next_mode = next(self.mode_gen)
            return DiskAccess(pos=next_pos, length=next_length, mode=next_mode)
        else:
            raise ValueError("Generators not set!")

def uniform_workload(length, disk_size, alignment):
    while True:
        pos = trunc(random.random() * (disk_size - length) / alignment) * alignment
        yield {
            "pos": pos,
            "length": length,
            "mode": DiskAccess.READ,
        }


class MixedWorkload(Workload):
    def __init__(self, workload1, workload2, ratio):
        """mix the two workloads by ratio:(1-ratio), 
            no check against whether the two workloads have the same disk size
            Usage:
                a = Workload()
                b = Workload()

                mixedWorkload = MixedWorkload(a, b, 0.6)

        """
        super().__init__()
        assert(isinstance(workload1, Workload))
        assert(isinstance(workload2, Workload))
        assert(isinstance(ratio, float))

        self.workload1 = workload1
        self.workload2 = workload2
        self.ratio = ratio

    def __next__(self):
        if random.random() <= self.ratio:
            return next(self.workload1)
        else:
            return next(self.workload2)


class MixedRWWorkload(Workload):
    def __init__(self, workload, read_ratio=1):
        super().__init__()
        """Random determine r/w for each access in a workload"""
        assert isinstance(workload, Workload)
        assert isinstance(read_ratio, float)

        assert read_ratio >= 0 and read_ratio <= 1

        self.workload = workload
        self.read_ratio = read_ratio

    def __next__(self):
        diskAccess = next(self.workload)

        if random.random() <= self.read_ratio:
            diskAccess.mode = DiskAccess.READ
        else:
            diskAccess.mode = DiskAccess.WRITE

        return diskAccess

def mix_rw(read_ratio=1):
    return lambda x: MixedRWWorkload(x, read_ratio)


class MostRecentWorkload(Workload):
    def __init__(self, workload0, n, eps, a=0.9):
        """
        a workload that may often revisit most recent `n` accesses
        Usage:
            workload = MostRecentWorkload(workload0, n=20, eps=0.9)

            Generates a workload that samples from the most recent 20 accesses with 0.9 probability,
            the distribution between most recent entries is according to zipf law
            and 0.1 probability from workload0
        """
        assert isinstance(workload0, Workload)
        assert isinstance(n, int)
        assert isinstance(eps, float)
        
        self.eps = eps
        self.workload0 = workload0
        self.n = n
        try:
            from zipfiangen import ZipfianGenerator
            self.zipfiangen = ZipfianGenerator(n=n, a=a)
        except ImportError:
            print("Most recent workload needs zipfian generator!")
            raise

    def __next__(self):
        if self.zipfiangen.empty or random.random() >= self.eps:
            entry = next(self.workload0)
            self.zipfiangen.update(entry)
            return entry
        else:
            return self.zipfiangen.sample()
