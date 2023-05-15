import json

from numpy import ndarray


class NumpyJsonEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
