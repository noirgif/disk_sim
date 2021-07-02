class DiskAccess:
    READ=0
    WRITE=1
    ACCESS_NAMES=("READ", "WRITE")

    def __init__(self, pos, length, mode=READ) -> None:
        assert(type(pos) is int)
        assert(type(length) is int)
        self.pos = pos
        self.length = length
        self.mode = mode
    
    def __repr__(self) -> str:
        return "DiskAccess({}, pos={}, length={})".format(
            self.__class__.ACCESS_NAMES[self.mode],
            self.pos,
            self.length
        )
    
    def is_valid(self):
        return self.pos >= 0 and self.length >= 0