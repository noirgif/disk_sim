Files:

- `access`: host the class that describes a disk access
- `disksim`: host classes that simulates the behavior of a disk
- `workload`: classes of workloads, which are generators of `DiskAccess`es

- In directory `util`:
        - `LRU`: a LRU cache
        - `size`: the `size` function provides a way to write human-readable sizes for disks
        - `zipfiangen`: a random generator that samples recent entries more often
