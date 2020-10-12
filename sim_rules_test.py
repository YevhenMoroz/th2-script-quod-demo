import google
import google.protobuf.empty_pb2

from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2, simulator_pb2_grpc
from grpc_modules import simulator_pb2
import grpc

# start rule
channel = grpc.insecure_channel('10.0.22.22:31977')
# channel = grpc.insecure_channel('localhost:8081')
simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(channel)

# DemoRule = simulator.createTemplateQuodDemoRule(
#     request=quod_simulator_pb2.TemplateQuodDemoRule(
#         connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child'),
#         demo_field1=123,
#         demo_field2='KCH_QA_RET_CHILD'))

# OCR = simulator.createQuodOCRRule(request=quod_simulator_pb2.TemplateQuodOCRRule(connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child')))

MDR_paris = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
    connection_id=infra_pb2.ConnectionID(session_alias="fix-feed-eq-paris"),
    sender="QUOD_UTP",
    md_entry_size={10000: 10000},
    md_entry_px={110: 100}))

MDR_trqx = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
    connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-eq-trqx"),
    sender="QUOD_UTP",
    md_entry_size={10000: 10000},
    md_entry_px={110: 100}))

# stop rule
core = simulator_pb2_grpc.ServiceSimulatorStub(channel)
# core.removeRule(DemoRule)
# # core.removeRule(OCR)
# channel.close()

# get rules
running_rules = core.getRulesInfo(request=google.protobuf.empty_pb2.Empty()).info
print(running_rules)
# remove rule
# for r in running_rules:
#     core.removeRule(simulator_pb2.RuleID(id=r.id.id))

core.removeRule(simulator_pb2.RuleID(id=8))

