from .serializer import Serializer


class StringSerializer(Serializer):

    def dump(self, value) -> bytes:
        return bytes(value, encoding='utf8')

    def load(self, bytes_to_load):
        return bytes_to_load.decode("utf-8")

