class LRU:
    """An LRU history"""
    def __init__(self, n):
        """
            n: the size of history
        """
        self.n = n
        # the history in a list,
        #   from the most recent to the least recent
        self.history = [None] * n

        # a set of entries for python performance reasons
        self.history_set = set()
        self.set_need_update = False
        # count of current valid members
        self.valid_cnt = 0
    
    def push(self, entry):
        """Update the history with a new entry"""
        # try moving the entry to the front, if present
        try:
            self.history.remove(entry)
        except ValueError:
            if self.valid_cnt == self.n:
                # need to make room for the new entry
                self.history.pop()
            else:
                self.valid_cnt += 1
            self.set_need_update = True

        self.history.insert(0, entry)
            
    
    def pop(self, entry):
        """Remove an entry from history"""
        try:
            self.history.remove(entry)
            self.history.append(None)
            self.valid_cnt -= 1
            self.set_need_update = True
        except ValueError:
            pass
    
    def _update_set(self):
        if self.set_need_update:
            # remove None entries, but no further filtering
            self.history_set = set(e for e in self.history if e)
            self.set_need_update = False

    def contains(self, entry):
        """Check whether an entry is in LRU"""
        self._update_set()
        return entry in self.history_set

    @property
    def empty(self):
        return self.valid_cnt == 0
    
    def __iter__(self):
        return self.history_set