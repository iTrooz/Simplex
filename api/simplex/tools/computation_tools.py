def init2DArray(columns: int, rows: int, content=None):
    arr = []
    for _ in range(rows):
        arr.append([content] * columns)
    return arr

def auto_str(cls):
    """
    From https://stackoverflow.com/a/33800620
    """
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls