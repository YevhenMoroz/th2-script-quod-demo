import grpc
from google.protobuf.empty_pb2 import Empty
from th2_grpc_sim_http.sim_template_pb2 import TemplateHttpLogonRule
from th2_grpc_sim import sim_pb2_grpc as core_http
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim.sim_pb2 import *

# start rules
simulator = Stubs.simulator_http
coreHttp = core_http.SimStub(grpc.insecure_channel("10.0.22.22:31123"))

Logon = simulator.createHttpLogonRule(request=TemplateHttpLogonRule(connection_id=ConnectionID(session_alias='http-server')))

# get rules
running_rules = coreHttp.getRulesInfo(request=Empty()).info
print(running_rules, "Rules running:", len(running_rules))
input()

# remove rules
coreHttp.removeRule(Logon)

# for i in range(3, 10):
#     coreHttp.removeRule(RuleID(id=i))

# for r in running_rules:
#     if r.id.id not in [1, 2]:
#         core.removeRule(RuleID(id=r.id.id))
