from abc import ABC, abstractmethod
from InvalidOperationError import InvalidOperationError


class Stream(ABC):
    def __init__(self):
        self.opened = False

    @abstractmethod
    def read(self):
        pass