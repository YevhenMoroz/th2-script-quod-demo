from google.protobuf.empty_pb2 import Empty
from stubs import Stubs
from th2_grpc_sim_quod.sim_pb2 import *
from th2_grpc_sim_quod.sim_service import *
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim.sim_pb2 import *

# start rule
simulator = Stubs.simulator

# DemoRule = simulator.createTemplateQuodDemoRule(
#     request=TemplateQuodDemoRule(
#         connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-RET-child'),
#         demo_field1=123,
# #         demo_field2='KCH_QA_RET_CHILD'))
#
# OCR = simulator.createQuodOCRRule(
#     request=TemplateQuodOCRRule(connection_id=ConnectionID(session_alias='fix-bs-eq-paris')))
#
# NOS = simulator.createQuodNOSRule(
#     request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias='fix-bs-eq-paris'), account="KEPLER"))


# RFQ = simulator.createQuodRFQRule(
#     request=TemplateQuodRFQRule(connection_id=ConnectionID(session_alias='fix-fh-fx-rfq')))

# TRFQ = simulator.createQuodRFQTRADERule(
#     request=TemplateQuodRFQTRADERule(connection_id=ConnectionID(session_alias='')))
#
# MDESP = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
#     connection_id=ConnectionID(session_alias="fix-fh-fx-esp"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))
#
# SingleExecParis = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
#     connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
#     no_party_ids=[
#             TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
#             TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
#             TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
#         ],
#     cum_qty=1000,
#     mask_as_connectivity="fix-fh-eq-paris",
#     md_entry_size={0: 1000},
#     md_entry_px={0: 30},
#     symbol="1062"
# ))
#
# SingleExecTrqx = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
#     connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
#     no_party_ids=[
#             TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
#             TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
#             TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
#         ],
#     cum_qty=100,
#     mask_as_connectivity="fix-fh-eq-trqx",
#     md_entry_size={900: 1000},
#     md_entry_px={40: 30},
#     symbol="3503"
# ))
#
# MDR_paris = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
#     connection_id=ConnectionID(session_alias="fix-fh-eq-paris"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))
#
#
# MDR_trqx = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
#     connection_id=ConnectionID(session_alias="fix-fh-eq-trqx"),
#     sender="QUOD_UTP",
#     md_entry_size={1000: 1000},
#     md_entry_px={40: 30}))


## Use Def Rules for debug only
# DefRule = simulator.createQuodDefMDRRule(request=quod_simulator_pb2.TemplateQuodDefMDRRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-eq-paris")
# ))
#
# DefRule1 = simulator.createQuodDefMDRRule1(request=quod_simulator_pb2.TemplateQuodDefMDRRule(
#     connection_id=infra_pb2.ConnectionID(session_alias="fix-fh-eq-trqx")
# ))
# StoreNOS = simulator.createQuodNOSStoreRule(
#     request=TemplateQuodNOSStoreRule(connection_id=ConnectionID(session_alias='fix-bs-eq-paris'), account="KEPLER"))

# stop rule
core = Stubs.core


# core.removeRule(OCR)
# core.removeRule(RFQ)
# core.removeRule(MDESP)
# core.removeRule(SingleExecParis)
# core.removeRule(SingleExecTrqx)
# core.removeRule(MDR_paris)
# core.removeRule(MDR_trqx)

#args={"field1":"value1","field2":"value2"}
# core.touchRule(request=TouchRequest(id=StoreNOS, args={"Symbol": "", "": ""}))
# core.removeRule(StoreNOS)
# get rules
running_rules = core.getRulesInfo(request=Empty()).info
print(running_rules, "Rules running:", len(running_rules))
# remove rule
for r in running_rules:
    if r.id.id not in [1, 2]:
        core.removeRule(RuleID(id=r.id.id))


MDRefID = simulator.getMDRefIDForConnection(request=RequestMDRefID(
    symbol="EUR/USD",
    connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
)).MDRefID

MDRefID303 = simulator.getMDRefIDForConnection303(request=RequestMDRefID(
    symbol="EUR/USD:FXF:YR1:HSBC",
    connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
)).MDRefID

allMDRefID = simulator.getAllMDRefID(request=RequestMDRefID(
    connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
))


for i in range(479,483):
    core.removeRule(RuleID(id=i))

