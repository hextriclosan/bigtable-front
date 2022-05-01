from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def dump(self, value) -> bytes:
        pass

    @abstractmethod
    def load(self, bytes_to_load):
        pass
