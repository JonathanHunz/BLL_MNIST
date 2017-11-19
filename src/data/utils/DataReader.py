from abc import ABC, abstractclassmethod


class DataReader(ABC):
    """Abstract class for an iterable file reader"""

    def __init__(self):
        super().__init__()

    def __iter__(self):
        return self

    @abstractclassmethod
    def next(self):
        pass
