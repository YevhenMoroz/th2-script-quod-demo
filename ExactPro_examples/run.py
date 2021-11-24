from google.protobuf.empty_pb2 import Empty
from stubs import Stubs
from th2_grpc_sim_quod import sim_pb2
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodRFQRule
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodRFQTRADERule
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodMDRRule
from th2_grpc_common.common_pb2 import ConnectionID

# start rule
simulator = Stubs.simulator

RFQ = simulator.createQuodRFQRule(
    request=TemplateQuodRFQRule(connection_id=ConnectionID(session_alias='fix-fh-fx-rfq')))

TRFQ = simulator.createQuodRFQTRADERule(
    request=TemplateQuodRFQTRADERule(connection_id=ConnectionID(session_alias='fix-fh-fx-rfq')))

MDESP = simulator.createQuodMDRRule(request=TemplateQuodMDRRule(
    connection_id=ConnectionID(session_alias="fix-fh-fx-esp"),
    sender="QUOD_UTP",
    md_entry_size={3000000: 3000000},
    md_entry_px={40: 30}))


# stop rule
core = Stubs.core

running_rules = core.getRulesInfo(request=Empty()).info
print(running_rules)
input()

core.removeRule(RFQ)
core.removeRule(TRFQ)
core.removeRule(MDESP)

core.removeRule(sim_pb2.RuleID(id=1))
