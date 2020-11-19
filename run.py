import google.protobuf.empty_pb2

from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2, simulator_pb2_grpc
from grpc_modules import simulator_pb2
import grpc

# start rule
channel = grpc.insecure_channel('10.0.22.22:31977')
simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(channel)

RFQ = simulator.createQuodRFQRule(request=quod_simulator_pb2.TemplateQuodRFQRule(connection_id=infra_pb2.ConnectionID(session_alias='fix-fh-fx-rfq')))

TRFQ = simulator.createQuodRFQTRADERule(request=quod_simulator_pb2.TemplateQuodRFQTRADERule(connection_id=infra_pb2.ConnectionID(session_alias='fix-fh-fx-rfq')))

MDESP = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
    connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-fx-esp"),
    sender="QUOD_UTP",
    md_entry_size={3000000: 3000000},
    md_entry_px={40: 30}))


# stop rule
core = simulator_pb2_grpc.ServiceSimulatorStub(channel)

running_rules = core.getRulesInfo(request=google.protobuf.empty_pb2.Empty()).info
print(running_rules)
input()

core.removeRule(RFQ)
core.removeRule(TRFQ)
core.removeRule(MDESP)

#core.removeRule(simulator_pb2.RuleID(id=i)