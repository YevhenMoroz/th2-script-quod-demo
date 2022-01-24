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


class RuleManager:

    def __init__(self):
        # Default rules IDs. Might be changed
        self.default_rules_id = [1, 3,  5, 6, 7, 8, 9, 10, 11]
        self.test_core = core_test.SimStub(grpc.insecure_channel("10.0.22.22:32314"))

    # Console output list of IDs active rules
    @staticmethod
    def print_active_rules():
        active_rules = dict()
        for rule in Stubs.core.getRulesInfo(request=Empty()).info:
            active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
        for key, value in active_rules.items():
            print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')

    @staticmethod
    def print_active_rules_sim_test():
        test_core = core_test.SimStub(grpc.insecure_channel("10.0.22.22:32314"))
        running_rules = test_core.getRulesInfo(request=Empty()).info
        print(f'Rules running(test_sim) :{len(running_rules)}')
        active_rules = dict()
        for rule in running_rules:
            active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
        for key, value in active_rules.items():
            if '.' in value[0]:
                print(f'{key} -> {value[0].split(".")[6]} -> {value[1]}')
            else:
                print(f'{key} -> {value[0]} -> {value[1]}')
        print('=' * 50)

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

    # Remove rule by ID
    # Example: 101
    def remove_rule_by_id_test_sim(self, rule_id: int):
        self.test_core.removeRule(RuleID(id=rule_id))

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

    @staticmethod
    def remove_rules(list_rules):
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

    # ------------------------

    # --- ADD RULE SECTION ---
    # Add rule on <session>
    # Example: session = 'fix-fh-fx-paris'

    @staticmethod
    def add_NewOrdSingleExecutionReportTrade(session: str, account: str, venue: str, price: float, traded_qty: int,
                                             delay: int):
        return Stubs.simulator.createNewOrdSingleExecutionReportTrade(
            request=TemplateNewOrdSingleExecutionReportTrade(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             venue=venue,
                                                             price=price,
                                                             tradedQty=traded_qty,
                                                             delay=delay))

    @staticmethod
    def add_NewOrdSingleExecutionReportTrade_FIXStandard(session: str, account: str, venue: str, price: float,
                                                        traded_qty: int,
                                                        delay: int):
        return Stubs.simulator.createNewOrdSingleExecutionReportTradeFIXStandard(
            request=TemplateNewOrdSingleExecutionReportTradeFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=venue,
                price=price,
                tradedQty=traded_qty,
                delay=delay))

    @staticmethod
    def add_NewOrdSingleExecutionReportTradeByOrdQty(session: str, account: str, exdestination: str, price: float,
                                                     traded_price: float, qty: int, traded_qty: int, delay: int):
        return Stubs.simulator.createNewOrdSingleExecutionReportTradeByOrdQty(
            request=TemplateNewOrdSingleExecutionReportTradeByOrdQty(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     exdestination=exdestination,
                                                                     price=price,
                                                                     traded_price=traded_price,
                                                                     qty=qty,
                                                                     traded_qty=traded_qty,
                                                                     delay=delay))

    @staticmethod
    def add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(session: str, account: str, exdestination: str,
                                                                 price: float,
                                                                 traded_price: float, qty: int, traded_qty: int,
                                                                 delay: int = 0):
        return Stubs.simulator.createNewOrdSingleExecutionReportTradeByOrdQtyFIXStandard(
            request=TemplateNewOrdSingleExecutionReportTradeByOrdQtyFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=exdestination,
                price=price,
                traded_price=traded_price,
                qty=qty,
                traded_qty=traded_qty,
                delay=delay))

    @staticmethod
    def add_NewOrdSingleExecutionReportPendingAndNew(session: str, account: str, venue: str, price: float):
        return Stubs.simulator.createNewOrdSingleExecutionReportPendingAndNew(
            request=TemplateNewOrdSingleExecutionReportPendingAndNew(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     venue=venue,
                                                                     price=price))

    @staticmethod
    def add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(session: str, account: str, venue: str, price: float):
        return Stubs.simulator.createNewOrdSingleExecutionReportPendingAndNewFIXStandard(
            request=TemplateNewOrdSingleExecutionReportPendingAndNewFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                venue=venue,
                price=price))

    @staticmethod
    def add_OrderCancelRequest(session: str, account: str, venue: str, cancel: bool):
        return Stubs.simulator.createOrderCancelRequest(
            request=TemplateOrderCancelRequest(connection_id=ConnectionID(session_alias=session),
                                               account=account,
                                               venue=venue,
                                               cancel=cancel))

    @staticmethod
    def add_OrderCancelRequest_FIXStandard(session: str, account: str, venue: str, cancel: bool):
        return Stubs.simulator.createOrderCancelRequestFIXStandard(
            request=TemplateOrderCancelRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=venue,
                                                          cancel=cancel))

    @staticmethod
    def add_NOS(session: str, account: str = 'KEPLER'):
        return Stubs.simulator.createQuodNOSRule(
            request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias=session), account=account))

    @staticmethod
    def add_OCR(session: str):
        return Stubs.simulator.createQuodOCRRule(request=
                                                 TemplateQuodOCRRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_OCRR(session: str, trade: bool = False):
        return Stubs.simulator.createQuodOCRRRule(request=
                                                  TemplateQuodOCRRRule(connection_id=
                                                                       ConnectionID(session_alias=session),
                                                                       trade=trade))

    @staticmethod
    def add_RFQ(session: str):
        return Stubs.simulator.createQuodRFQRule(request=
                                                 TemplateQuodRFQRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_RFQ_test_sim(session: str):
        return Stubs.test_sim.createQuodRFQRule(request=
                                                TemplateQuodRFQRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_TRFQ(session: str):
        return Stubs.simulator.createQuodRFQTRADERule(request=
                                                      TemplateQuodRFQTRADERule(connection_id=
                                                                               ConnectionID(session_alias=session)))

    @staticmethod
    def add_TRFQ_test_sim(session: str):
        return Stubs.test_sim.createQuodRFQTRADERule(request=
                                                     TemplateQuodRFQTRADERule(connection_id=
                                                                              ConnectionID(session_alias=session)))

    @staticmethod
    def add_TRADE_ESP(session: str):
        return Stubs.simulator.createQuodESPTradeRule(request=
                                                      TemplateQuodESPTradeRule(connection_id=
                                                                               ConnectionID(session_alias=session)))

    @staticmethod
    def add_TRADE_ESP_test(session: str):
        return Stubs.test_sim.createQuodESPTradeRule(request=
                                                     TemplateQuodESPTradeRule(connection_id=
                                                                              ConnectionID(session_alias=session)))

    @staticmethod
    def add_QuodMDAnswerRule(session: str, interval: int):
        return Stubs.simulator.createQuodMDAnswerRule(request=
                                                      TemplateMDAnswerRule(connection_id=
                                                                           ConnectionID(session_alias=session), min=1,
                                                                           max=2, interval=30))

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
    def add_NewOrdSingle_FOK(session: str, account: str, venue: str, trade: bool, price: float):
        return Stubs.simulator.createNewOrdSingleFOK(
            request=TemplateNewOrdSingleFOK(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            price=price))

    @staticmethod
    def add_NewOrdSingle_FOK_FIXStandard(session: str, account: str, venue: str, trade: bool, price: float):
        return Stubs.simulator.createNewOrdSingleFOKFIXStandard(
            request=TemplateNewOrdSingleFOKFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       exdestination=venue,
                                                       trade=trade,
                                                       price=price))

    @staticmethod
    def add_NewOrdSingle_IOC(session: str, account: str, venue: str, trade: bool, tradedQty: int, price: float):
        return Stubs.simulator.createNewOrdSingleIOC(
            request=TemplateNewOrdSingleIOC(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            tradedQty=tradedQty,
                                            price=price
                                            ))

    @staticmethod
    def add_NewOrdSingle_IOC_FIXStandard(session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                         price: float):
        return Stubs.simulator.createNewOrdSingleIOCFIXStandard(
            request=TemplateNewOrdSingleIOCFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       exdestination=venue,
                                                       trade=trade,
                                                       tradedQty=tradedQty,
                                                       price=price
                                                       ))

    @staticmethod
    def add_MarketNewOrdSingle_IOC(session: str, account: str, venue: str, trade: bool, tradedQty: int, price: float):
        return Stubs.simulator.createMarketNewOrdSingleIOC(
            request=TemplateMarketNewOrdSingleIOC(connection_id=ConnectionID(session_alias=session),
                                                  account=account,
                                                  venue=venue,
                                                  trade=trade,
                                                  tradedQty=tradedQty,
                                                  price=price
                                                  ))

    @staticmethod
    def add_MarketNewOrdSingle_IOC_FIXStandard(session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                               price: float):
        return Stubs.simulator.createMarketNewOrdSingleIOCFIXStandard(
            request=TemplateMarketNewOrdSingleIOCFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             exdestination=venue,
                                                             trade=trade,
                                                             tradedQty=tradedQty,
                                                             price=price
                                                             ))

    @staticmethod
    def add_NewOrdSingle_Market(session: str, account: str, venue: str, trade: bool, tradedQty: int, avgPrice: float):
        return Stubs.simulator.createNewOrdSingleMarket(
            request=TemplateNewOrdSingleMarket(connection_id=ConnectionID(session_alias=session),
                                               account=account,
                                               venue=venue,
                                               trade=trade,
                                               tradedQty=tradedQty,
                                               avgPrice=avgPrice
                                               ))

    @staticmethod
    def add_NewOrdSingle_Market_FIXStandard(session: str, account: str, venue: str, trade: bool, tradedQty: int,
                                            avgPrice: float):
        return Stubs.simulator.createNewOrdSingleMarketFIXStandard(
            request=TemplateNewOrdSingleMarketFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=venue,
                                                          trade=trade,
                                                          tradedQty=tradedQty,
                                                          avgPrice=avgPrice
                                                          ))

    @staticmethod
    def add_OrderCancelReplaceRequest_ExecutionReport(session: str, trade: bool):
        return Stubs.simulator.createOrderCancelReplaceExecutionReport(
            request=TemplateOrderCancelReplaceExecutionReport(connection_id=ConnectionID(session_alias=session),
                                                              trade=trade
                                                              ))

    @staticmethod
    def add_OrderCancelReplaceRequest(session: str, account: str, exdestination: str, modify=True):
        return Stubs.simulator.createOrderCancelReplaceRequest(
            request=TemplateOrderCancelReplaceRequest(connection_id=ConnectionID(session_alias=session),
                                                      account=account,
                                                      exdestination=exdestination,
                                                      modify=modify
                                                      ))

    @staticmethod
    def add_OrderCancelReplaceRequest_FIXStandard(session: str, account: str, exdestination: str, modify=True):
        return Stubs.simulator.createOrderCancelReplaceRequestFIXStandard(
            request=TemplateOrderCancelReplaceRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                                 account=account,
                                                                 exdestination=exdestination,
                                                                 modify=modify
                                                                 ))

    @staticmethod
    def add_NewOrderSingle_ExecutionReport_Reject(session: str, account: str, ex_destination: str, price: float):
        return Stubs.simulator.createNewOrdSingleExecutionReportReject(
            request=TemplateNewOrdSingleExecutionReportReject(connection_id=ConnectionID(session_alias=session),
                                                              account=account,
                                                              exdestination=ex_destination,
                                                              price=price
                                                              ))

    @staticmethod
    def add_fx_md_to(session: str):
        return Stubs.simulator.createQuodDefMDRFXRule(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_fx_md_to_test_sim(session: str):
        return Stubs.test_sim.createQuodDefMDRFXRule(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

    @staticmethod
    def add_MarketNewOrdSingle_FOK(session: str, account: str, venue: str, price: float, trade: bool):
        return Stubs.simulator.createMarketNewOrdSingleFOK(
            request=TemplateMarketNewOrdSingleFOK(connection_id=ConnectionID(session_alias=session),
                                                  account=account,
                                                  venue=venue,
                                                  trade=trade,
                                                  price=price
                                                  ))

    @staticmethod
    def add_MarketNewOrdSingle_FOK(session: str, account: str, venue: str, price: float, trade: bool):
        return Stubs.simulator.createMarketNewOrdSingleFOKFIXStandard(
            request=TemplateMarketNewOrdSingleFOKFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             exdestination=venue,
                                                             trade=trade,
                                                             price=price
                                                             ))

    @staticmethod
    def add_NewOrdSingle_IOC_MarketData(session: str, account: str, exdestination: str, price: float, tradedQty: int,
                                        trade: bool, sessionAlias: str, symbol: str,
                                        triggerPrice: float, triggerQty: int, snapshotFullRefresh, incrementalRefresh):
        return Stubs.simulator.createNewOrdSingleIOCMarketData(
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
    rule_manager = RuleManager()
    # nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard('fix-buy-317-standard-test',
    #                                                                                  'XPAR_CLIENT1', 'XPAR',
    #                                                                                 float(20))
    # nos_rule = rule_manager.add_NewOrdSingle_Market_FIXStandard('fix-buy-317-standard-test',
    #                                                             'CLIENT_YMOROZ_PARIS', 'XPAR', False, 100, 10.0)
    # nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard("fix-buy-317-standard-test", "XPAR_CLIENT1",
    #                                                                      "XPAR", float(20))
    # rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard("fix-buy-317-standard-test", "XPAR_CLIENT1", "XPAR",
    #                                                               float(20), 100, 1)
    rule_manager.remove_rules_by_id_range(95,98)
    # rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-317-standard-test', 'XPAR_CLIENT1', 'XPAR',
    #                                                           10)
    rule_manager.print_active_rules()
