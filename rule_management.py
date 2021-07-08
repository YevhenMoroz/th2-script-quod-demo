from th2_grpc_sim_quod.sim_pb2 import (TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule,
                                       TemplateQuodRFQRule, TemplateQuodRFQTRADERule, TemplateQuodSingleExecRule,
                                       TemplateNewOrdSingleExecutionReportTrade,
                                       TemplateNewOrdSingleExecutionReportPendingAndNew, TemplateQuodDefMDRRule)
from th2_grpc_sim.sim_pb2 import RuleID
from th2_grpc_common.common_pb2 import ConnectionID

from stubs import Stubs
from google.protobuf.empty_pb2 import Empty


class RuleManager:

    def __init__(self):
        # Default rules IDs
        self.default_rules_id = [1, 2, 3, 4, 5, 6, 7]
        for rule in Stubs.core.getRulesInfo(request=Empty()).info:
            rule_id = rule.id.id
            if rule_id in [3, 4] or rule.class_name.count('Quod_Def_MDR_Rule') > 0:
                self.default_rules_id.append(rule_id)

    # Console output list of IDs active rules
    @staticmethod
    def print_active_rules():
        active_rules = dict()
        for rule in Stubs.core.getRulesInfo(request=Empty()).info:
            active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
        for key, value in active_rules.items():
            print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')

    # --- REMOVE RULES SECTION ---

    # Remove all rules except defaults
    def remove_all_rules(self):
        for rule in Stubs.core.getRulesInfo(request=Empty()).info:
            rule_id = rule.id.id
            if rule_id not in self.default_rules_id:
                Stubs.core.removeRule(RuleID(id=rule_id))

    # Remove rules that contains <remove_rule_name>
    # <session> - optional parameter
    # Example: remove_rule_name = 'NOS' -> remove all rules that name contains 'NOS'
    def remove_rules_by_name(self, remove_rule_name: str, session=None):
        if session is not None:
            for rule in Stubs.core.getRulesInfo(request=Empty()).info:
                rule_id = rule.id.id
                if rule_id not in self.default_rules_id \
                        and rule.class_name.count(remove_rule_name) == 1 \
                        and session == rule.connection_id.session_alias:
                    Stubs.core.removeRule(RuleID(id=rule_id))
        else:
            for rule in Stubs.core.getRulesInfo(request=Empty()).info:
                rule_id = rule.id.id
                if rule_id not in self.default_rules_id and rule.class_name.count(remove_rule_name) == 1:
                    Stubs.core.removeRule(RuleID(id=rule_id))

    # Remove rule by ID
    # Example: 101
    def remove_rule_by_id(self, rule_id: int):
        if rule_id not in self.default_rules_id:
            Stubs.core.removeRule(RuleID(id=rule_id))

    # Remove rules by list of ID
    # Example: [101, 203, 204, 303]
    def remove_rules_by_id_list(self, rules_id_list: list):
        for i in rules_id_list:
            if i not in self.default_rules_id:
                Stubs.core.removeRule(RuleID(id=i))

    # Remove rules by range of ID
    # Example: [101; 201]
    def remove_rules_by_id_range(self, id_start_range: int, id_end_range: int):
        for i in range(id_start_range, id_end_range):
            if i not in self.default_rules_id:
                Stubs.core.removeRule(RuleID(id=i))

    # Remove user-created rule
    # Example:
    # new_rule = RuleManager.add_NOS('fix-fh-fx-paris')
    # RuleManager.remove_rule(new_rule)
    @staticmethod
    def remove_rule(rule):
        Stubs.core.removeRule(rule)

    # ------------------------

    # --- ADD RULE SECTION ---
    # Add rule on <session>
    # Example: session = 'fix-fh-fx-paris'

    @staticmethod
    def add_NewOrdSingleExecutionReportTrade(session: str, account: str, venue: str, price: int, traded_qty: int,
                                             delay: int, ):
        return Stubs.simulator.createNewOrdSingleExecutionReportTrade(
            request=TemplateNewOrdSingleExecutionReportTrade(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             venue=venue,
                                                             price=price,
                                                             tradedQty=traded_qty,
                                                             delay=delay))

    @staticmethod
    def add_NewOrdSingleExecutionReportPendingAndNew(session: str, account: str, venue: str, price: int):
        return Stubs.simulator.createNewOrdSingleExecutionReportPendingAndNew(
            request=TemplateNewOrdSingleExecutionReportPendingAndNew(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     venue=venue,
                                                                     price=price))

    @staticmethod
    def add_NOS(session: str, account: str = 'KEPLER'):
        return Stubs.simulator.createQuodNOSRule(
            request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias=session), account=account))

    @staticmethod
    def add_OCR(session: str):
        return Stubs.simulator.createQuodOCRRule(request=
                                                 TemplateQuodOCRRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_OCRR(session: str):
        return Stubs.simulator.createQuodOCRRRule(request=
                                                  TemplateQuodOCRRRule(connection_id=
                                                                       ConnectionID(session_alias=session)))

    @staticmethod
    def add_RFQ(session: str):
        return Stubs.simulator.createQuodRFQRule(request=
                                                 TemplateQuodRFQRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_TRFQ(session: str):
        return Stubs.simulator.createQuodRFQTRADERule(request=
                                                      TemplateQuodRFQTRADERule(connection_id=
                                                                               ConnectionID(session_alias=session)))

    @staticmethod
    def add_SingleExec(party_id, cum_qty, md_entry_size, md_entry_px, symbol, session: str, mask_as_connectivity: str):
        return Stubs.simulator.createQuodSingleExecRule(
            request=TemplateQuodSingleExecRule(
                connection_id=ConnectionID(session_alias=session),
                no_party_ids=party_id,
                cum_qty=cum_qty,
                mask_as_connectivity=mask_as_connectivity,
                md_entry_size=md_entry_size,
                md_entry_px=md_entry_px,
                symbol=symbol))

    @staticmethod
    def add_fx_md_to(session: str):
        return Stubs.simulator.createQuodDefMDRFXRule(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

    # -----


if __name__ == '__main__':
    rule_manager = RuleManager()
    # rule_manager.remove_all_rules()
    rule_manager.print_active_rules()
    Stubs.factory.close()
