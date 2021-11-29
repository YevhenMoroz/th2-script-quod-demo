import grpc
from google.protobuf.empty_pb2 import Empty
from th2_grpc_sim_http.sim_template_pb2 import TemplateHttpLogonRule, TemplateHttpAnswerRule, PartySettlement1, \
    PartySettlement2, SettlementInstructions1, SettlementInstructions2, TemplateDeleteRule
from th2_grpc_sim import sim_pb2_grpc as core_http
from stubs import Stubs

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim.sim_pb2 import *

# start rules
simulator = Stubs.simulator_http
coreHttp = core_http.SimStub(grpc.insecure_channel("10.0.22.22:31123"))

Logon = simulator.createHttpLogonRule(request=TemplateHttpLogonRule(connection_id=ConnectionID(session_alias='http-server')))
Delete = simulator.createDeleteRule(request=TemplateDeleteRule(connection_id=ConnectionID(session_alias='http-server')))

Answer = simulator.createHttpAnswerRule(
    request=TemplateHttpAnswerRule(
        connection_id=ConnectionID(session_alias='http-server'),
        instructingPartyValue="BLMACHAL2XX",
        settlementInstructions={"ID1": "BT01C", "SubAccountNo": "21435", "PaymentCurrency": "GBP", "SubAgentBIC": "RTBSGB2LXXX",
                                "SubAgentName1": "RBC INVESTOR SERVICES TRUST, UK BRA", "SubAgentName2": "NCH",
                                "PSET": "CRSTGB22", "InstitutionBIC": "OMGOUS33XXX", "ParticipantName1": "OMGEO LLC"},
        matchingSecurityCode="FI-25061620",
        account1ID="3434",
        account2ID="ACC-2",
        partySettlement1=PartySettlement1(SettlementInstructionsSourceIndicator="ALRT",
                                          AlertCountryCode="GBR",
                                          AlertMethodType="CREST",
                                          AlertSecurityType="EQU",
                                          AlertSettlementModelName="INTMODEL",
                                          settlementInstructions=SettlementInstructions1(ID1="BT01C",
                                                                                         SubAccountNo="21435",
                                                                                         PaymentCurrency="GBP",
                                                                                         SubAgentBIC="RTBSGB2LXXX",
                                                                                         SubAgentName1="RBC INVESTOR SERVICES TRUST, UK BRA",
                                                                                         SubAgentName2="NCH",
                                                                                         PSET="CRSTGB22",
                                                                                         InstitutionBIC="OMGOUS33XXX",
                                                                                         ParticipantName1="OMGEO LLC",
                                                                                         )),
        partySettlement2=PartySettlement2(SettlementInstructionsSourceIndicator="ALRT",
                                          AlertCountryCode="USA",
                                          AlertMethodType="DTC",
                                          AlertSecurityType="EQU",
                                          AlertSettlementModelName="ARALERTI",
                                          settlementInstructions=SettlementInstructions2(ID1="1940",
                                                                                         ID2="00053308",
                                                                                         ID3="00058320",
                                                                                         SecurityAccount="23438",
                                                                                         SubAccountNo="100527",
                                                                                         PaymentCurrency="USD",
                                                                                         CashAccountNo="23438",
                                                                                         SubAgentBIC="DTCCUS41XXX",
                                                                                         SubAgentName1="DEPOSITORY TRUST AND CLEARING CORPO",
                                                                                         SubAgentName2="RATION",
                                                                                         PSET="DTCYUS33",
                                                                                         AffirmingPartyIndicator="A",
                                                                                         InstitutionBIC="OMGOUS33XXX"
                                                                                         )),
    ))




# get rules
running_rules = coreHttp.getRulesInfo(request=Empty()).info
print(running_rules, "Rules running:", len(running_rules))
input()

# remove rules
coreHttp.removeRule(Logon)
coreHttp.removeRule(Answer)
coreHttp.removeRule(Delete)

# for i in range(3, 10):
#     coreHttp.removeRule(RuleID(id=i))

# for r in running_rules:
#     if r.id.id not in [1, 2]:
#         core.removeRule(RuleID(id=r.id.id))
