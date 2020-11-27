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

# OCR = simulator.createQuodOCRRule(request=quod_simulator_pb2.TemplateQuodOCRRule(connection_id=infra_pb2.ConnectionID(session_alias='fix-bs-eq-paris')))

# RFQ = simulator.createQuodRFQRule(request=quod_simulator_pb2.TemplateQuodRFQRule(connection_id=infra_pb2.ConnectionID(session_alias='fix-fh-fx-rfq')))
#
# TRFQ = simulator.createQuodRFQTRADERule(request=quod_simulator_pb2.TemplateQuodRFQTRADERule(connection_id=infra_pb2.ConnectionID(session_alias='')))
#
# MDESP = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-fx-esp"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))
#
# SingleExecParis = simulator.createQuodSingleExecRule(request=quod_simulator_pb2.TemplateQuodSingleExecRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-bs-eq-paris"),
#     no_party_ids=[
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
#         ],
#     cum_qty=1000,
#     mask_as_connectivity="fix-fh-eq-paris",
#     md_entry_size={0: 1000},
#     md_entry_px={0: 30},
#     symbol="1062"
# ))
#
# SingleExecTrqx = simulator.createQuodSingleExecRule(request=quod_simulator_pb2.TemplateQuodSingleExecRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-bs-eq-trqx"),
#     no_party_ids=[
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
#             quod_simulator_pb2.TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
#         ],
#     cum_qty=100,
#     mask_as_connectivity="fix-fh-eq-trqx",
#     md_entry_size={900: 1000},
#     md_entry_px={40: 30},
#     symbol="3503"
# ))
#
# MDR_paris = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-eq-paris"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))
#
#
# MDR_trqx = simulator.createQuodMDRRule(request=quod_simulator_pb2.TemplateQuodMDRRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-eq-trqx"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))

# stop rule
core = simulator_pb2_grpc.ServiceSimulatorStub(channel)
# core.removeRule(DemoRule)
# # core.removeRule(OCR)
# channel.close()

# get rules
running_rules = core.getRulesInfo(request=google.protobuf.empty_pb2.Empty()).info
print(running_rules)
# # remove rule
for r in running_rules:
    core.removeRule(simulator_pb2.RuleID(id=r.id.id))

# for i in range(69,81):
#     core.removeRule(simulator_pb2.RuleID(id=i))

