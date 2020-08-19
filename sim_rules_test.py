from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2
from grpc_modules import simulator_pb2
import grpc

simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(grpc.insecure_channel('localhost:8081'))
print(simulator.createQuodNOSRule(request=quod_simulator_pb2.TemplateQuodNOSRule(connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child'))))
# print(simulator.createRule_FIX(request=quod_simulator_pb2.TemplateFixCreate(fields = {"a":infra_pb2.Value(simple_value="123")}, connection_id=infra_pb2.ConnectionID(session_alias="123"))))
