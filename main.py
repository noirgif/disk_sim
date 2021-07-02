"""Demonstrate the use of the workload and the cache"""

from disksim import Cache
from workload import MostRecentWorkload, MixedRWWorkload, CustomWorkload, mix_rw, uniform_workload
from size import size
from math import ceil

block_size = size(K=32)
disk_size = size(G=1)
block_num = ceil(disk_size / block_size)

cache = Cache(block_size=block_size, cache_size=block_num)

# create a workload:
# it samples from uniform workload 50% of the time
# and from the most recent 30 entries 50% of the time
# with 50% read, 50% write
workload = CustomWorkload(
                all_gen=uniform_workload(length=block_size,
                        disk_size=disk_size, alignment=block_size))

workload = MostRecentWorkload(workload0=workload, n=30, eps=0.5)
workload = MixedRWWorkload(workload, read_ratio=0.5)

for diskAccess in workload:
        result = cache.handle(diskAccess, admit=True)
        print(diskAccess, "  HITS:", result)