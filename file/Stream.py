from abc import ABC, abstractmethod
from InvalidOperationError import InvalidOperationError


class Stream(ABC):
    def __init__(self):
        self.opened = False

    def open(self):
        if self.opened:
            raise InvalidOperationError('Sream is already opened')
        self.opened = True

    def close(self):
        if not self.opened:
            raise InvalidOperationError('Sream is already closed')
        self.opened = False

    @abstractmethod
    def read(self):
        pass