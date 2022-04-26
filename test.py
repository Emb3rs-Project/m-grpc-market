import jsonpickle

from manager.manager_pb2 import StartSimulationRequest
from ms_grpc.plibs.manager.manager_models import StartSimulationRequestModel

a = StartSimulationRequestModel()

_dict = {
    "xpto": 1,
    "data": "x",
    "array": [1, ",", 3]
}

inputs = {
    "simulation_uuid": 'xpto',
    "simulation_metadata": jsonpickle.encode(_dict, unpicklable=True)
}

grpc_request = StartSimulationRequest(
    **inputs
)

a.from_grpc(grpc_request)

print(a)

print(type([]).__name__)

b = [1, 2, 3, { "a" : 2}, 5, 6]
b_j = jsonpickle.encode(b, unpicklable=True)

print(type(b_j).__name__)
print(b_j)

c: list = []
c = jsonpickle.decode(b_j)

print(type(c).__name__)
print(c)
