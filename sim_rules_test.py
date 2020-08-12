from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2, simulator_pb2_grpc
from grpc_modules import simulator_pb2
import grpc

#start rule
channel = grpc.insecure_channel('localhost:8081')
simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(channel)
QuodRuleID = simulator.createQuodNOSRule(request=quod_simulator_pb2.TemplateQuodNOSRule(connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child')))
print(QuodRuleID)
# stop rule
# core = simulator_pb2_grpc.ServiceSimulatorStub(channel)
# core.removeRule(QuodRuleID)