from scipy.stats import zipfian

class ZipfianGenerator:
    def __init__(self, n, a):
        """
            n: the size of history
            a: the zipfian constant
        """
        self.a = a
        self.n = n
        self.history = [None] * n
        # count of current valid members
        self.valid_cnt = 0
    
    def update(self, entry):
        """Update the history with a new entry"""
        # delete previous entry
        need_pop_entry = False
        try:
            self.history.remove(entry)
        except ValueError:
            if self.valid_cnt == self.n:
                # need to make room
                self.history.pop()
            else:
                self.valid_cnt += 1

        self.history.insert(0, entry)
            
    
    def invalidate(self, entry):
        try:
            self.history.remove(entry)
            self.history.append(None)
            self.valid_cnt -= 1
        except ValueError:
            pass

    def sample(self, update=True):
        """Sample a recent entry
            update: if this entry count as recent entries(and update the history)
        """
        no = zipfian.rvs(self.a, self.valid_cnt)
        entry = self.history[no - 1]
        if update:
            self.update(entry)
        
        return entry
    
    @property
    def empty(self):
        return self.valid_cnt == 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.sample()