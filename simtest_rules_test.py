import grpc
from google.protobuf.empty_pb2 import Empty
from th2_grpc_sim_http.sim_template_pb2 import TemplateHttpLogonRule
from th2_grpc_sim import sim_pb2_grpc as core_test
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim.sim_pb2 import *

# start rules
simulator = Stubs.test_sim
coreTest = core_test.SimStub(grpc.insecure_channel("10.0.22.22:32314"))

# OCR = simulator.createQuodOCRRule(
#     request=TemplateQuodOCRRule(connection_id=ConnectionID(session_alias='fix-bs-eq-paris')))

# get rules
running_rules = coreTest.getRulesInfo(request=Empty()).info
print(running_rules, "Rules running:", len(running_rules))
input()

# remove rules
coreTest.removeRule()

# for i in range(3, 10):
#     coreTest.removeRule(RuleID(id=i))

# for r in running_rules:
#     if r.id.id not in [1, 2]:
#         coreTest.removeRule(RuleID(id=r.id.id))
