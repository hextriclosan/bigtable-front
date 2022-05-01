from abc import abstractmethod

from .serializer import Serializer


class IntegerSerializer(Serializer):

    def dump(self, value) -> bytes:
        return int(value).to_bytes(self.get_integer_size(), byteorder=self.get_endianess(), signed=self.is_signed())

    def load(self, bytes_to_load):
        return int.from_bytes(bytes_to_load, byteorder=self.get_endianess(), signed=self.is_signed())

    @abstractmethod
    def get_integer_size(self):
        pass

    @abstractmethod
    def get_endianess(self):
        pass

    @abstractmethod
    def is_signed(self):
        pass
