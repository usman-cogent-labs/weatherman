from abc import ABC, abstractmethod


class Stream(ABC):
    @abstractmethod
    def read(self):
        pass
