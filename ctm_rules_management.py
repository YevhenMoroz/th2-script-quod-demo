from google.protobuf.empty_pb2 import Empty
from th2_grpc_sim.sim_pb2 import RuleID
from th2_grpc_sim_http_quod.sim_template_pb2 import TemplateHttpLogonRule, TemplateHttpAnswerRule, PartySettlement1, \
    PartySettlement2, SettlementInstructions1, SettlementInstructions2, TemplateDeleteRule
from stubs import Stubs

from th2_grpc_common.common_pb2 import ConnectionID


# region rules
class CTMRuleManager:
    def __init__(self, session_alias='http-server'):
        self.session_alias = session_alias
        self.default_rules = [1]

    def print_active_rules(self):
        active_rules = {
            rule.id.id: [rule.class_name, rule.connection_id.session_alias]
            for rule in Stubs.core_ctm.getRulesInfo(request=Empty()).info
        }
        for key, value in active_rules.items():
            print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')

    def remove_all_rules(self):
        for rule in Stubs.core_ctm.getRulesInfo(request=Empty()).info:
            rule_id = rule.id.id
            if rule_id not in self.default_rules:
                Stubs.core_ctm.removeRule(RuleID(id=rule_id))


    def remove_rule(self, rule):
        Stubs.core_ctm.removeRule(rule)

    def remove_rules(self, list_rules: list):
        for rule in list_rules:
            self.remove_rule(rule)

    def remove_rule_by_id(self, rule_id: int):
        if rule_id not in self.default_rules:
            Stubs.core_ctm.removeRule(RuleID(id=rule_id))

    def remove_rules_by_id_list(self, rules_id_list: list):
        for i in rules_id_list:
            if i not in self.default_rules:
                Stubs.core_ctm.removeRule(RuleID(id=i))

    def remove_rules_by_id_range(self, id_start_range: int, id_end_range: int):
        for i in range(id_start_range, id_end_range):
            if i not in self.default_rules:
                Stubs.core_ctm.removeRule(RuleID(id=i))

    def add_login_rule(self):
        return Stubs.simulator_http.createHttpLogonRule(
            request=TemplateHttpLogonRule(connection_id=ConnectionID(session_alias=self.session_alias)))

    def add_delete_rule(self):
        return Stubs.simulator_http.createDeleteRule(
            request=TemplateDeleteRule(connection_id=ConnectionID(session_alias=self.session_alias)))

    # this rule will be triggered if the incoming Put request contains: TradeLevelInformation,TradeCommFeesTaxes,
    # TLEBSettlement, InstructingParty, ExecutingBroker, MasterReference
    def add_autoresponder_with_2_acc(self, account_1, account_2):
        return Stubs.simulator_http.createHttpAnswerRule(
            request=TemplateHttpAnswerRule(
                connection_id=ConnectionID(session_alias=self.session_alias),
                instructingPartyValue="QUODTESTGW3",
                settlementInstructions={"ID1": "BT01C", "SubAccountNo": "21435", "PaymentCurrency": "EUR",
                                        "SubAgentBIC": "AUTOIM01XXX",
                                        "SubAgentName1": "RBC INVESTOR SERVICES TRUST, UK BRA", "SubAgentName2": "NCH",
                                        "PSET": "EURO_CLEAR", "InstitutionBIC": "AUTOIM01XXX",
                                        "ParticipantName1": "OMGEO LLC"},
                matchingSecurityCode="FR0010436584",
                account1ID=account_1,
                account2ID=account_2,
                partySettlement1=PartySettlement1(SettlementInstructionsSourceIndicator="ALRT",
                                                  AlertCountryCode="GBR",
                                                  AlertMethodType="CREST",
                                                  AlertSecurityType="EQU",
                                                  AlertSettlementModelName="INTMODEL",
                                                  settlementInstructions=SettlementInstructions1(ID1="BT01C",
                                                                                                 SubAccountNo="21435",
                                                                                                 PaymentCurrency="EUR",
                                                                                                 SubAgentBIC="AUTOIM01XXX",
                                                                                                 SubAgentName1="RBC INVESTOR SERVICES TRUST, UK BRA",
                                                                                                 SubAgentName2="NCH",
                                                                                                 PSET="EURO_CLEAR",
                                                                                                 InstitutionBIC="AUTOIM01XXX",
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
                                                                                                 SubAgentBIC="AUTOIM01XXX",
                                                                                                 SubAgentName1="DEPOSITORY TRUST AND CLEARING CORPO",
                                                                                                 SubAgentName2="RATION",
                                                                                                 PSET="EURO_CLEAR",
                                                                                                 AffirmingPartyIndicator="A",
                                                                                                 InstitutionBIC="AUTOIM01XXX"
                                                                                                 )),
            ))


# endregion

if __name__ == '__main__':
    rule_manager = CTMRuleManager()
    rule_manager.print_active_rules()
    # rule_manager.remove_all_rules()
    Stubs.factory.close()
