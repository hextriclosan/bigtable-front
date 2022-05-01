from .string import StringSerializer
from .java_integer import JavaIntegerSerializer
from .java_long import JavaLongSerializer

PLUGINS = {
    "String": StringSerializer(),
    "JavaInteger": JavaIntegerSerializer(),
    "JavaLong": JavaLongSerializer()
}


def get_serializer(name):
    return PLUGINS[name]
