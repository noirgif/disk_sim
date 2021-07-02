from access import DiskAccess
from math import trunc, ceil
from LRU import LRU
import heapq

class Disk:
    def __init__(self) -> None:
        pass

    def handle(self, diskAccess: DiskAccess):
        return 1


def diskAccess2Blocks(diskAccess, block_size):
    """
    Given a DiskAccess and the block size, return the blocks accessed
    """
    start = trunc(diskAccess.pos / block_size)
    if (diskAccess.pos + diskAccess.length) % block_size == 0:
        last = round((diskAccess.pos + diskAccess.length) / block_size)
    else:
        last = ceil((diskAccess.pos + diskAccess.length) / block_size)
    return tuple(range(start, last))


class Cache:
    def __init__(self, block_size, cache_size) -> None:
        self.visited = LRU(cache_size)
        self.block_size = block_size
        self.cache_size = cache_size
    
    def handle(self, diskAccess: DiskAccess, admit: bool):
        """Handles a disk access, that may span several blocks,
           return the number of blocks hit. If `admit` is set, the cache
           is updated with this access.
           
           Note: the number of blocks depend on the disk access itself,
                as well as the block size of the cache
        """
        blockAccess = diskAccess2Blocks(diskAccess, self.block_size)
        result = 0
        
        for block in blockAccess:    
            if self.visited.contains(block):
                result += 1
            
            if admit:
                self.visited.push(block)
        
        return result


if __name__ == '__main__':
    from size import size
    diskaccesses = [DiskAccess(pos=size(K=64), length=size(K=4)), 
        DiskAccess(pos=size(K=65), length=size(K=4)),
        DiskAccess(pos=size(K=128), length=size(K=64))]
    
    for diskaccess in diskaccesses:
        print(diskaccess, diskAccess2Blocks(diskaccess, size(K=4)))