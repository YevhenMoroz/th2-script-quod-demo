import grpc
from google.protobuf.empty_pb2 import Empty
from th2_grpc_sim_http.sim_template_pb2 import TemplateHttpLogonRule
from th2_grpc_sim import sim_pb2_grpc as core_test
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodDefMDRRule

from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim.sim_pb2 import *

# start rules
simulator = Stubs.test_sim

coreTest = core_test.SimStub(grpc.insecure_channel("10.0.22.22:32314"))

# get rules
running_rules = coreTest.getRulesInfo(request=Empty()).info

print(f'Rules running(test_sim) :{len(running_rules)}')
active_rules = dict()
for rule in running_rules:
    active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
for key, value in active_rules.items():
    print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')

# # remove rule
# for r in running_rules:
#     if r.id.id not in [1, 2]:
#         core.removeRule(RuleID(id=1))
# coreTest.removeRule(RuleID(id=1))
# Stubs.test_sim.cre(request= TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))


# MDRefID = simulator.getMDRefIDForConnection(request=RequestMDRefID(
#     symbol="EUR/USD",
#     connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
# )).MDRefID
#
# MDRefID303 = simulator.getMDRefIDForConnection303(request=RequestMDRefID(
#     symbol="EUR/USD:FXF:YR1:HSBC",
#     connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
# )).MDRefID
#
# allMDRefID = simulator.getAllMDRefID(request=RequestMDRefID(
#     connection_id=ConnectionID(session_alias="fix-fh-fx-esp")
# ))
#
#
# for i in range(479,483):
#     core.removeRule(RuleID(id=i))
#
