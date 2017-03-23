from json import JSONEncoder


class BufferJsonEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, buffer):
            return obj[0:-1]
        return super(BufferJsonEncoder, self).default(obj)
