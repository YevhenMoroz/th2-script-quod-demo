from enum import Enum

from th2_grpc_sim_fix_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule, \
    TemplateQuodRFQRule, TemplateQuodRFQTRADERule, TemplateQuodSingleExecRule, TemplateNoPartyIDs, \
    TemplateNewOrdSingleExecutionReportTrade, TemplateNewOrdSingleExecutionReportPendingAndNew, TemplateNewOrdSingleIOC, \
    TemplateNewOrdSingleFOK, TemplateOrderCancelRequest, TemplateNewOrdSingleMarket, \
    TemplateOrderCancelReplaceExecutionReport, TemplateOrderCancelReplaceRequest, \
    TemplateNewOrdSingleExecutionReportTradeByOrdQty, TemplateNewOrdSingleExecutionReportReject, \
    TemplateMarketNewOrdSingleFOK, TemplateQuodDefMDRRule, TemplateNewOrdSingleIOCMarketData, \
    TemplateMarketNewOrdSingleIOC, TemplateQuodESPTradeRule, TemplateMDAnswerRule, \
    TemplateNewOrdSingleExecutionReportPendingAndNewFIXStandard, \
    TemplateNewOrdSingleExecutionReportTradeByOrdQtyFIXStandard, TemplateNewOrdSingleExecutionReportTradeFIXStandard, \
    TemplateNewOrdSingleMarketFIXStandard, TemplateOrderCancelRequestFIXStandard, TemplateNewOrdSingleFOKFIXStandard, \
    TemplateNewOrdSingleIOCFIXStandard, TemplateMarketNewOrdSingleIOCFIXStandard, \
    TemplateOrderCancelReplaceRequestFIXStandard, TemplateMarketNewOrdSingleFOKFIXStandard
from th2_grpc_sim.sim_pb2 import RuleID
from th2_grpc_common.common_pb2 import ConnectionID

from stubs import Stubs
from google.protobuf.empty_pb2 import Empty
import grpc
from th2_grpc_sim import sim_pb2_grpc as core_test


class Simulators(Enum):
    default = {"core": Stubs.core, "sim": Stubs.simulator, "default_rules": [1, 3, 5, 6, 7, 8, 9, 10, 11]}
    equity = {"core": Stubs.core_equity, "sim": Stubs.simulator_equity, "default_rules": [1, 2, 3, 4]}


class RuleManager:

    def __init__(self, sim=Simulators.default):
        # Default rules IDs. Might be changed
        self.default_rules_id = sim.value["default_rules"]
        self.sim = sim.value["sim"]
        self.core = sim.value["core"]

    # Console output list of IDs active rules
    def print_active_rules(self):
        active_rules = dict()
        for rule in self.core.getRulesInfo(request=Empty()).info:
            active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
        for key, value in active_rules.items():
            print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')

    # --- REMOVE RULES SECTION ---

    # Remove all rules except defaults
    def remove_all_rules(self):
        for rule in self.core.getRulesInfo(request=Empty()).info:
            rule_id = rule.id.id
            if rule_id not in self.default_rules_id:
                self.core.removeRule(RuleID(id=rule_id))

    # Remove rules that contains <remove_rule_name>
    # <session> - optional parameter
    # Example: remove_rule_name = 'NOS' -> remove all rules that name contains 'NOS'
    def remove_rules_by_name(self, remove_rule_name: str, session=None):
        if session is not None:
            for rule in self.core.getRulesInfo(request=Empty()).info:
                rule_id = rule.id.id
                if rule_id not in self.default_rules_id \
                        and rule.class_name.count(remove_rule_name) == 1 \
                        and session == rule.connection_id.session_alias:
                    self.core.removeRule(RuleID(id=rule_id))
        else:
            for rule in self.core.getRulesInfo(request=Empty()).info:
                rule_id = rule.id.id
                if rule_id not in self.default_rules_id and rule.class_name.count(remove_rule_name) == 1:
                    self.core.removeRule(RuleID(id=rule_id))

    # Remove rule by ID
    # Example: 101

    def remove_rule_by_id(self, rule_id: int):
        if rule_id not in self.default_rules_id:
            self.core.removeRule(RuleID(id=rule_id))

    # Remove rule by ID

    # Remove rules by list of ID
    # Example: [101, 203, 204, 303]
    def remove_rules_by_id_list(self, rules_id_list: list):
        for i in rules_id_list:
            if i not in self.default_rules_id:
                self.core.removeRule(RuleID(id=i))

    # Remove rules by range of ID
    # Example: [101; 201]
    def remove_rules_by_id_range(self, id_start_range: int, id_end_range: int):
        for i in range(id_start_range, id_end_range):
            if i not in self.default_rules_id:
                self.core.removeRule(RuleID(id=i))

    # Remove user-created rule
    # Example:
    # new_rule = RuleManager.add_NOS('fix-fh-fx-paris')
    # RuleManager.remove_rule(new_rule)

    def remove_rule(self, rule):
        self.core.removeRule(rule)

    def remove_rules(self, list_rules):
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

    # ------------------------

    # --- ADD RULE SECTION ---
    # Add rule on <session>
    # Example: session = 'fix-fh-fx-paris'
    def add_NewOrdSingleExecutionReportTrade(self, session: str, account: str, venue: str, price: float,
                                             traded_qty: int,
                                             delay: int):
        return self.sim.createNewOrdSingleExecutionReportTrade(
            request=TemplateNewOrdSingleExecutionReportTrade(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             venue=venue,
                                                             price=price,
                                                             tradedQty=traded_qty,
                                                             delay=delay))

    def add_NewOrdSingleExecutionReportTrade_FIXStandard(self, session: str, account: str, venue: str, price: float,
                                                         traded_qty: int,
                                                         delay: int):
        return self.sim.createNewOrdSingleExecutionReportTradeFIXStandard(
            request=TemplateNewOrdSingleExecutionReportTradeFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=venue,
                price=price,
                tradedQty=traded_qty,
                delay=delay))

    def add_NewOrdSingleExecutionReportTradeByOrdQty(self, session: str, account: str, exdestination: str, price: float,
                                                     traded_price: float, qty: int, traded_qty: int, delay: int):
        return self.sim.createNewOrdSingleExecutionReportTradeByOrdQty(
            request=TemplateNewOrdSingleExecutionReportTradeByOrdQty(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     exdestination=exdestination,
                                                                     price=price,
                                                                     traded_price=traded_price,
                                                                     qty=qty,
                                                                     traded_qty=traded_qty,
                                                                     delay=delay))

    def add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self, session: str, account: str, exdestination: str,
                                                                 price: float,
                                                                 traded_price: float, qty: int, traded_qty: int,
                                                                 delay: int = 0):
        return self.sim.createNewOrdSingleExecutionReportTradeByOrdQtyFIXStandard(
            request=TemplateNewOrdSingleExecutionReportTradeByOrdQtyFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=exdestination,
                price=price,
                traded_price=traded_price,
                qty=qty,
                traded_qty=traded_qty,
                delay=delay))

    def add_NewOrdSingleExecutionReportPendingAndNew(self, session: str, account: str, venue: str, price: float):
        return self.sim.createNewOrdSingleExecutionReportPendingAndNew(
            request=TemplateNewOrdSingleExecutionReportPendingAndNew(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     venue=venue,
                                                                     price=price))

    def add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self, session: str, account: str, venue: str,
                                                                 price: float):
        return self.sim.createNewOrdSingleExecutionReportPendingAndNewFIXStandard(
            request=TemplateNewOrdSingleExecutionReportPendingAndNewFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                venue=venue,
                price=price))

    def add_OrderCancelRequest(self, session: str, account: str, venue: str, cancel: bool):
        return self.sim.createOrderCancelRequest(
            request=TemplateOrderCancelRequest(connection_id=ConnectionID(session_alias=session),
                                               account=account,
                                               venue=venue,
                                               cancel=cancel))

    def add_OrderCancelRequest_FIXStandard(self, session: str, account: str, venue: str, cancel: bool):
        return self.sim.createOrderCancelRequestFIXStandard(
            request=TemplateOrderCancelRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=venue,
                                                          cancel=cancel))

    def add_NOS(self, session: str, account: str = 'KEPLER'):
        return self.sim.createQuodNOSRule(
            request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias=session), account=account))

    def add_OCR(self, session: str):
        return self.sim.createQuodOCRRule(request=
                                          TemplateQuodOCRRule(connection_id=ConnectionID(session_alias=session)))

    def add_OCRR(self, session: str, trade: bool = False):
        return self.sim.createQuodOCRRRule(request=
                                           TemplateQuodOCRRRule(connection_id=
                                                                ConnectionID(session_alias=session),
                                                                trade=trade))

    def add_RFQ(self, session: str):
        return self.sim.createQuodRFQRule(request=
                                          TemplateQuodRFQRule(connection_id=ConnectionID(session_alias=session)))

    def add_TRFQ(self, session: str):
        return self.sim.createQuodRFQTRADERule(request=
                                               TemplateQuodRFQTRADERule(connection_id=
                                                                        ConnectionID(session_alias=session)))

    def add_TRADE_ESP(self, session: str):
        return self.sim.createQuodESPTradeRule(request=
                                               TemplateQuodESPTradeRule(connection_id=
                                                                        ConnectionID(session_alias=session)))

    def add_TRADE_ESP_test(self, session: str):
        return self.sim.createQuodESPTradeRule(request=
                                               TemplateQuodESPTradeRule(connection_id=
                                                                        ConnectionID(session_alias=session)))

    def add_QuodMDAnswerRule(self, session: str):
        return self.sim.createQuodMDAnswerRule(request=
                                               TemplateMDAnswerRule(connection_id=
                                                                    ConnectionID(session_alias=session), min=1,
                                                                    max=2, interval=30))

    def add_SingleExec(self, party_id, cum_qty, md_entry_size, md_entry_px, symbol, session: str,
                       mask_as_connectivity: str):
        return self.sim.createQuodSingleExecRule(
            request=TemplateQuodSingleExecRule(
                connection_id=ConnectionID(session_alias=session),
                no_party_ids=party_id,
                cum_qty=cum_qty,
                mask_as_connectivity=mask_as_connectivity,
                md_entry_size=md_entry_size,
                md_entry_px=md_entry_px,
                symbol=symbol))

    def add_NewOrdSingle_FOK(self, session: str, account: str, venue: str, trade: bool, price: float):
        return self.sim.createNewOrdSingleFOK(
            request=TemplateNewOrdSingleFOK(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            price=price))

    def add_NewOrdSingle_FOK_FIXStandard(self, session: str, account: str, venue: str, trade: bool, price: float, ):
        return self.sim.createNewOrdSingleFOKFIXStandard(
            request=TemplateNewOrdSingleFOKFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       exdestination=venue,
                                                       trade=trade,
                                                       price=price))

    def add_NewOrdSingle_IOC(self, session: str, account: str, venue: str, trade: bool, tradedQty: int, price: float):
        return self.sim.createNewOrdSingleIOC(
            request=TemplateNewOrdSingleIOC(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            tradedQty=tradedQty,
                                            price=price
                                            ))

    def add_NewOrdSingle_IOC_FIXStandard(self, session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                         price: float):
        return self.sim.createNewOrdSingleIOCFIXStandard(
            request=TemplateNewOrdSingleIOCFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       exdestination=venue,
                                                       trade=trade,
                                                       tradedQty=tradedQty,
                                                       price=price
                                                       ))

    def add_MarketNewOrdSingle_IOC(self, session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                   price: float):
        return self.sim.createMarketNewOrdSingleIOC(
            request=TemplateMarketNewOrdSingleIOC(connection_id=ConnectionID(session_alias=session),
                                                  account=account,
                                                  venue=venue,
                                                  trade=trade,
                                                  tradedQty=tradedQty,
                                                  price=price
                                                  ))

    def add_MarketNewOrdSingle_IOC_FIXStandard(self, session: str, account: str, venue: str, trade: bool,
                                               tradedQty: int,
                                               price: float):
        return self.sim.createMarketNewOrdSingleIOCFIXStandard(
            request=TemplateMarketNewOrdSingleIOCFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             exdestination=venue,
                                                             trade=trade,
                                                             tradedQty=tradedQty,
                                                             price=price
                                                             ))

    def add_NewOrdSingle_Market(self, session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                avgPrice: float):
        return self.sim.createNewOrdSingleMarket(
            request=TemplateNewOrdSingleMarket(connection_id=ConnectionID(session_alias=session),
                                               account=account,
                                               venue=venue,
                                               trade=trade,
                                               tradedQty=tradedQty,
                                               avgPrice=avgPrice
                                               ))

    def add_NewOrdSingle_Market_FIXStandard(self, session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                            avgPrice: float):
        return self.sim.createNewOrdSingleMarketFIXStandard(
            request=TemplateNewOrdSingleMarketFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=venue,
                                                          trade=trade,
                                                          tradedQty=tradedQty,
                                                          avgPrice=avgPrice
                                                          ))

    def add_OrderCancelReplaceRequest_ExecutionReport(self, session: str, trade: bool):
        return self.sim.createOrderCancelReplaceExecutionReport(
            request=TemplateOrderCancelReplaceExecutionReport(connection_id=ConnectionID(session_alias=session),
                                                              trade=trade
                                                              ))

    def add_OrderCancelReplaceRequest(self, session: str, account: str, exdestination: str, modify=True):
        return self.sim.createOrderCancelReplaceRequest(
            request=TemplateOrderCancelReplaceRequest(connection_id=ConnectionID(session_alias=session),
                                                      account=account,
                                                      exdestination=exdestination,
                                                      modify=modify
                                                      ))

    def add_OrderCancelReplaceRequest_FIXStandard(self, session: str, account: str, exdestination: str, modify=True):
        return self.sim.createOrderCancelReplaceRequestFIXStandard(
            request=TemplateOrderCancelReplaceRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                                 account=account,
                                                                 exdestination=exdestination,
                                                                 modify=modify
                                                                 ))

    def add_NewOrderSingle_ExecutionReport_Reject(self, session: str, account: str, ex_destination: str, price: float):
        return self.sim.createNewOrdSingleExecutionReportReject(
            request=TemplateNewOrdSingleExecutionReportReject(connection_id=ConnectionID(session_alias=session),
                                                              account=account,
                                                              exdestination=ex_destination,
                                                              price=price
                                                              ))

    def add_fx_md_to(self, session: str):
        return self.sim.createQuodDefMDRFXRule(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

    def add_MarketNewOrdSingle_FOK(self, session: str, account: str, venue: str, price: float, trade: bool):
        return self.sim.createMarketNewOrdSingleFOK(
            request=TemplateMarketNewOrdSingleFOK(connection_id=ConnectionID(session_alias=session),
                                                  account=account,
                                                  venue=venue,
                                                  trade=trade,
                                                  price=price
                                                  ))

    @staticmethod
    def add_MarketNewOrdSingle_FOK_FIXStandard(self, session: str, account: str, venue: str, price: float, trade: bool):
        return self.sim.createMarketNewOrdSingleFOKFIXStandard(
            request=TemplateMarketNewOrdSingleFOKFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             exdestination=venue,
                                                             trade=trade,
                                                             price=price
                                                             ))

    def add_NewOrdSingle_IOC_MarketData(self, session: str, account: str, exdestination: str, price: float,
                                        tradedQty: int,
                                        trade: bool, sessionAlias: str, symbol: str,
                                        triggerPrice: float, triggerQty: int, snapshotFullRefresh, incrementalRefresh):
        return self.sim.createNewOrdSingleIOCMarketData(
            request=TemplateNewOrdSingleIOCMarketData(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=exdestination,
                price=price,
                tradedQty=tradedQty,
                trade=trade,
                sessionAlias=sessionAlias,
                symbol=symbol,
                triggerPrice=triggerPrice,
                triggerQty=triggerQty,
                snapshotFullRefresh=snapshotFullRefresh,
                incrementalRefresh=incrementalRefresh,
            )
        )
    # ------------------------


if __name__ == '__main__':
    rule_manager = RuleManager(Simulators.equity)
    rule_manager.print_active_rules()
