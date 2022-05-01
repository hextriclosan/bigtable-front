from .integer_serializer import IntegerSerializer


class JavaIntegerSerializer(IntegerSerializer):

    def get_integer_size(self):
        return 4

    def get_endianess(self):
        return 'big'

    def is_signed(self):
        return True
