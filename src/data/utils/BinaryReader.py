import gzip
from .DataReader import DataReader


class BinaryReader(DataReader):
    def __init__(self, path, element_count, element_size, offset=0):
        super().__init__()

        self.element_count = element_count
        self.element_size = element_size

        self.index = 0

        # Open file as binary stream
        stream = gzip.open(path)
        # Skip offset bytes
        stream.read(offset)
        self.stream = stream

    def next(self):
        # Read and return next element
        if self.index < self.element_count:
            self.index += 1
            return self.stream.read(self.element_size)
        else:
            raise StopIteration
