from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc
from grpc_modules import simulator_pb2
import grpc

simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(grpc.insecure_channel('10.44.74.110:63342'))
print(simulator.createQuodNOSRule(request=simulator_pb2.RuleID(id=1)))
