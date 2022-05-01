from .integer_serializer import IntegerSerializer


class JavaLongSerializer(IntegerSerializer):

    def get_integer_size(self):
        return 8

    def get_endianess(self):
        return 'big'

    def is_signed(self):
        return True
