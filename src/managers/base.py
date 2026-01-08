from abc import ABC, abstractmethod


class BaseManager(ABC):
    @abstractmethod
    def write(self, url: str, short_code: str):
        pass

    @abstractmethod
    def read(self, short_code: str) -> str:
        pass

    @abstractmethod
    def create(self):
        pass
