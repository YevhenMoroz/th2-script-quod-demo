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
    TemplateOrderCancelReplaceRequestFIXStandard, TemplateMarketNewOrdSingleFOKFIXStandard, \
    TemplateNewOrdSingleExecutionReportRejectWithReason, TemplateNewOrdSingleExecutionReportEliminate, \
    TemplateOrderCancelReplaceRequestWithDelayFIXStandard, \
    TemplateExecutionReportTradeByOrdQtyWithLastLiquidityIndFIXStandard, \
    TemplateNewOrdSingleRQFRestated, TemplateNewOrdSingleMarketAuction, \
    TemplateOrderCancelRFQRequest, TemplateNewOrdSingleExecutionReportEliminateFixStandard, \
    TemplateOrderCancelRequestWithQty, TemplateNewOrdSingleRQFRejected, TemplateNewOrdSingleExecutionReportOnlyPending, \
    TemplateNewOrdSingleMarketPreviouslyQuoted, \
    TemplateOrderCancelReplaceExecutionReportWithTrade, TemplateOrderCancelRequestTradeCancel, \
    TemplateOrderCancelRFQRequest, \
    TemplateNewOrdSingleExecutionReportEliminateFixStandard, \
    TemplateOrderCancelRequestWithQty, TemplateNewOrdSingleRQFRejected, TemplateNewOrdSingleExecutionReportOnlyPending, \
    TemplateExternalExecutionReport, TemplateNewOrdSingleExecutionReportTradeByOrdQtyRBCustom, \
    TemplateNOSExecutionReportTradeWithTradeDateFIXStandard, TemplateNewOrdSingleIOCTradeOnFullQty, \
    TemplateNewOrdSingleExecutionReportDoneForDay, TemplateNewOrdSingleIOCTradeByOrderQty, TemplateFXOrderReject, TemplateNewOrdSingleTradeOnFullQty, TemplateNewOrdSingleExecutionReportAll, TemplateNewOrdSingleExecutionReportIOCAll, TemplateMarketDataRequestWithTimeout

from th2_grpc_sim.sim_pb2 import RuleID
from th2_grpc_common.common_pb2 import ConnectionID

from stubs import Stubs
from google.protobuf.empty_pb2 import Empty


class Simulators(Enum):
    default = {"core": Stubs.core, "sim": Stubs.simulator,
               "default_rules": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
    equity = {"core": Stubs.core_equity, "sim": Stubs.simulator_equity, "default_rules": [1, 2]}
    algo = {"core": Stubs.core_algo, "sim": Stubs.simulator_algo, "default_rules": [1, 2, 3]}


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

    def remove_rules_by_alias(self, alias: str):
        active_rules = dict()
        for rule in self.core.getRulesInfo(request=Empty()).info:
            active_rules[rule.id.id] = [rule.class_name, rule.connection_id.session_alias]
            if rule.connection_id.session_alias == alias and rule.id.id not in self.default_rules_id:
                self.core.removeRule(RuleID(id=rule.id.id))

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

    def remove_rules(self, list_rules: list):
        for rule in list_rules:
            self.remove_rule(rule)

    # ------------------------

    # --- ADD RULE SECTION ---
    # Add rule on <session>
    # Example: session = 'fix-fh-fx-paris'

    def add_MDRule(self, session: str):
        return self.sim.createQuodDefMDRRule2(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

    def add_SecurityStatusRule(self, session: str):
        return self.sim.createSecurityStatusRule(
            request=TemplateQuodDefMDRRule(connection_id=ConnectionID(session_alias=session)))

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
                                                     traded_price: float, qty: int, traded_qty: int, delay: int = 0):
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

    def add_NewOrdSingleExecutionReportPendingAndNew(self, session: str, account: str, venue: str, price: float, delay: int = 0):
        return self.sim.createNewOrdSingleExecutionReportPendingAndNew(
            request=TemplateNewOrdSingleExecutionReportPendingAndNew(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     venue=venue,
                                                                     price=price,
                                                                     delay=delay))

    def add_NewOrdSingleExecutionReportOnlyPending(self, session: str, account: str, venue: str, price: float):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all except IOC, FOK.
        By parameters: Account, ExDestination, Price.

        Result Message: ExecutionReport PendingNew.

        Description: Used for answer only with the execution report PendingNew to the NewOrderSingle message.

        Use cases: Very useful when we need to answer only with the execution report PendingNew to the NewOrderSingle message.
        """
        return self.sim.createNewOrdSingleExecutionReportOnlyPending(
            request=TemplateNewOrdSingleExecutionReportOnlyPending(connection_id=ConnectionID(session_alias=session),
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

    def add_NewOrdSingleExecutionReportTradeByOrdQtyWithTradeDate_FIXStandard(self, session: str, account: str,
                                                                              venue: str,
                                                                              price: float, traded_qty: int,
                                                                              tradeDate: str, delay: int):
        return self.sim.createNOSExecutionReportTradeWithTradeDateFIXStandard(
            request=TemplateNOSExecutionReportTradeWithTradeDateFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=venue,
                price=price,
                tradedQty=traded_qty,
                tradeDate=tradeDate,
                delay=delay))

    def add_OrderCancelRequest(self, session: str, account: str, venue: str, cancel: bool, delay: int = 0):
        return self.sim.createOrderCancelRequest(
            request=TemplateOrderCancelRequest(connection_id=ConnectionID(session_alias=session),
                                               account=account,
                                               venue=venue,
                                               cancel=cancel,
                                               delay=delay))

    def add_OrderCancelRequestTradeCancel(self, session: str, account: str, exdestination: str, price: float):
        return self.sim.createTemplateOrderCancelRequestTradeCancel(
            request=TemplateOrderCancelRequestTradeCancel(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=exdestination,
                                                          price=price))

    def add_OrderCancelRequestWithQty(self, session: str, account: str, venue: str, cancel: bool, qty: int,
                                      delay: int = 0):
        """
        Triggered on Message: OrderCancelRequest.
        By parameters: Account, ExDestination, OrderQty

        Additional input parameters: cancel: bool.

        Result Message: ExecutionReport Cancelled or OrderCancelReject (based on value of the 'cancel' parameter).

        Description: Used for answer with the execution report Cancelled for child with definite qty. Possible to set up delay for the answer.

        Use cases:
        1. When we have two or more orders on the same venue with the different qty and one order should be cancelled and it should be the CancelReject for the 2nd order.
        2. When we have two or more orders on the same venue with the different qty, and only one order should be cancelled.
        3. For the MPDark + Spray: if need to Cancel the 1st order on the venue for the rebalancing and not Cancel the 2nd order on the same venue after the rebalance.
        """
        return self.sim.createOrderCancelRequestWithQty(
            request=TemplateOrderCancelRequestWithQty(connection_id=ConnectionID(session_alias=session),
                                                      account=account,
                                                      venue=venue,
                                                      cancel=cancel,
                                                      qty=qty,
                                                      delay=delay))

    def add_OrderCancelRequest_FIXStandard(self, session: str, account: str, venue: str, cancel: bool):
        return self.sim.createOrderCancelRequestFIXStandard(
            request=TemplateOrderCancelRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                          account=account,
                                                          exdestination=venue,
                                                          cancel=cancel))

    def add_NOS(self, session: str, account: str = 'KEPLER'):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: all
        by parameters: Account

        Result Message: ExecutionReport New or ExecutionReport  Canceled (for IOC)

        Description: Send ExecReport with status New on 35=D with Text = 'sim work'. There is no PendingNew. For IOC orders - ExecReport Cancel

        Use cases: Use as basic rule for manual testing/ debugging when we need reply for orders with any Venue, TIF and Price

        Note: rule provided by ExactPro
       """
        return self.sim.createQuodNOSRule(
            request=TemplateQuodNOSRule(connection_id=ConnectionID(session_alias=session), account=account))

    def add_OCR(self, session: str):
        """
        Triggered on Message: OrderCancelRequest

        Result Message: ExecutionReport  Canceled

        Description: Reply on Cancel Request with ExecReport Canceled with Text = 'order canceled'

        Use cases: Use for RB testcases that don't use ExDestination in ER

        Note: rule provided by ExactPro
       """
        return self.sim.createQuodOCRRule(request=
                                          TemplateQuodOCRRule(connection_id=ConnectionID(session_alias=session)))

    def add_OCRR(self, session: str, trade: bool = False):
        """
        Triggered on Message: OrderCancelReplaceRequest
        by parameters: trade

        Result Message: ExecutionReport  Replaced or ExecutionReport Trade or ExecutionReport Canceled

        Description:
        1. Answer ER with replaced on the OrderCancelReplaceRequest with TIF not equals IOC or FOK orders and Trade=False
        2. Answer ER with full Fill on the OrderCancelReplaceRequest with TIF equals IOC or FOK orders and Trade=True
        3. Answer ER Canceled on the OrderCancelReplaceRequest with TIF equals IOC or FOK orders and Trade=False

        Use cases:
        1. To modify orders with any TIF exclude IOC and FOK
        2. To fully Fill the order with TIF equals IOC or FOK order
        3. To cancel IOC or FOK order

        Note: rule provided by ExactPro
        Also have add_OrderCancelReplaceRequest and add_OrderCancelReplaceRequest_ExecutionReport.
        Difference for IOC, FOK orders: trade:false, add_OCRR: ER Canceled, add_OrderCancelReplaceRequest_ExecutionReport: ER Replaced, ER Canceled
        add_OrderCancelReplaceRequest used for Redburn, Kepler tests
       """
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

    def add_External_Cancel(self, session: str):
        return self.sim.createExternalExecutionReportResponseCancelled(request=
                                                                       TemplateExternalExecutionReport(connection_id=
                                                                                                       ConnectionID(
                                                                                                           session_alias=session)))

    def add_External_Fill(self, session: str):
        return self.sim.createExternalExecutionReportResponseFilled(request=
                                                                    TemplateExternalExecutionReport(connection_id=
                                                                                                    ConnectionID(
                                                                                                        session_alias=session)))

    def add_External_Reject(self, session: str):
        return self.sim.createExternalExecutionReportResponseRejected(request=
                                                                      TemplateExternalExecutionReport(connection_id=
                                                                                                      ConnectionID(
                                                                                                          session_alias=session)))

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

    def add_NewOrdSingle_FOK(self, session: str, account: str, venue: str, trade: bool, price: float, delay: int = 0):
        return self.sim.createNewOrdSingleFOK(
            request=TemplateNewOrdSingleFOK(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            price=price,
                                            delay=delay))

    def add_NewOrdSingle_FOK_FIXStandard(self, session: str, account: str, venue: str, trade: bool, price: float, ):
        return self.sim.createNewOrdSingleFOKFIXStandard(
            request=TemplateNewOrdSingleFOKFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       exdestination=venue,
                                                       trade=trade,
                                                       price=price))

    def add_NewOrdSingle_IOC(self, session: str, account: str, venue: str, trade: bool, tradedQty: int, price: float,
                             delay: int = 0):
        return self.sim.createNewOrdSingleIOC(
            request=TemplateNewOrdSingleIOC(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            tradedQty=tradedQty,
                                            price=price,
                                            delay=delay
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

    def add_OrderCancelReplaceRequest_ExecutionReport(self, session: str, trade: bool, delay: int = 0):
        return self.sim.createOrderCancelReplaceExecutionReport(
            request=TemplateOrderCancelReplaceExecutionReport(connection_id=ConnectionID(session_alias=session),
                                                              trade=trade,
                                                              delay=delay
                                                              ))

    def add_OrderCancelReplaceRequest(self, session: str, account: str, exdestination: str, modify=True, delay=0):
        """
        Triggered on Message: OrderCancelReplaceRequest.
        By parameters: Account, ExDestination.

        Additional input parameters: modify: bool.

        Result Message: ExecutionReport Replaced or OrderCancelReject ModifyReject (based on value of the 'modify' parameter).

        Description: Differ from the add_OrderCancelReplaceRequest_ExecutionReport in that the in this rule it possible to select ExDestination and set up modifying or not.

        Use cases: Useful for cases when have several modification requests: accept one, reject another.
        """
        return self.sim.createOrderCancelReplaceRequest(
            request=TemplateOrderCancelReplaceRequest(connection_id=ConnectionID(session_alias=session),
                                                      account=account,
                                                      exdestination=exdestination,
                                                      modify=modify,
                                                      delay=delay
                                                      ))

    def add_OrderCancelReplaceRequest_FIXStandard(self, session: str, account: str, exdestination: str, modify=True):
        return self.sim.createOrderCancelReplaceRequestFIXStandard(
            request=TemplateOrderCancelReplaceRequestFIXStandard(connection_id=ConnectionID(session_alias=session),
                                                                 account=account,
                                                                 exdestination=exdestination,
                                                                 modify=modify
                                                                 ))

    def add_NewOrderSingle_ExecutionReport_Reject(self, session: str, account: str, ex_destination: str, price: float):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all.
        By parameters: Account, ExDestination, Price.

        Result Message: ExecutionReport Reject.

        Description: Used for answer with the ExecutionReport Reject without defining the reason.

        Use cases: Answer with the ExecutionReport Reject without defining the reason.

        Notes: Doesn't work in the Kepler tests.
        """
        return self.sim.createNewOrdSingleExecutionReportReject(
            request=TemplateNewOrdSingleExecutionReportReject(connection_id=ConnectionID(session_alias=session),
                                                              account=account,
                                                              exdestination=ex_destination,
                                                              price=price
                                                              ))

    def add_NewOrderSingle_ExecutionReport_RejectFX(self, session: str, account: str, ex_destination:str):
        return self.sim.createTemplateFXOrderReject(
            request=TemplateFXOrderReject(connection_id=ConnectionID(session_alias=session),
                                                              account=account,
                                                              exdestination=ex_destination
                                                              ))

    def add_NewOrderSingle_ExecutionReport_RejectWithReason(self, session: str, account: str, ex_destination: str,
                                                            price: float, reason: int, text: str = "QATestReject",
                                                            delay: int = 0):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all.
        By parameters: Account, ExDestination, Price.

        Additional input parameters: Text.

        Result Message: ExecutionReport Reject.

        Description: Differ from the add_NewOrderSingle_ExecutionReport_Reject in that the OrdRejReason presents in the ExecutionReportReject. And it is possible to setup the delay for the answer.

        Use cases: Very useful when we need that the OrdRejReason presents in the ExecutionReportReject.
        """
        return self.sim.createNewOrdSingleExecutionReportRejectWithReason(
            request=TemplateNewOrdSingleExecutionReportRejectWithReason(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=ex_destination,
                price=price,
                reason=reason,
                text=text,
                delay=delay
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

    def add_NewOrderSingle_ExecutionReport_Eliminate(self, session: str, account: str, ex_destination: str,
                                                     price: float, delay: int = 0, text: str = "order eliminated"):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all.
        By parameters: Account, ExDestination, Price.

        Additional input parameters: Text.

        Result Message: ExecutionReport Eliminate.

        Description: Used for answer with the ExecutionReport Eliminate regardless of TIF. It is possible to set up delay for the answer.

        Use cases: Very useful when we need to answer with the execution report Eliminate to the NewOrderSingle message regardless of TIF.
        """
        return self.sim.createNewOrdSingleExecutionReportEliminate(
            request=TemplateNewOrdSingleExecutionReportEliminate(connection_id=ConnectionID(session_alias=session),
                                                                 account=account,
                                                                 exdestination=ex_destination,
                                                                 price=price,
                                                                 delay=delay,
                                                                 text=text
                                                                 ))

    def add_OrderCancelReplaceRequestWithDelayFixStandard(self, session: str, account: str, ex_destination: str,
                                                          modify: bool, delay: int):
        return self.sim.createOrderCancelReplaceRequestWithDelayFIXStandard(
            request=TemplateOrderCancelReplaceRequestWithDelayFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=ex_destination,
                modify=modify,
                delay=delay))

    def add_ExecutionReportTradeByOrdQtyWithLastLiquidityInd_FIXStandard(self, session: str, account: str,
                                                                         ex_destination: str, price: float,
                                                                         traded_price: float,
                                                                         qty: int, traded_qty: int, delay: int,
                                                                         last_liquidity_ind):
        return self.sim.createExecutionReportTradeByOrdQtyWithLastLiquidityIndFIXStandard(
            request=TemplateExecutionReportTradeByOrdQtyWithLastLiquidityIndFIXStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=ex_destination,
                price=price,
                traded_price=traded_price,
                qty=qty,
                traded_qty=traded_qty,
                delay=delay,
                last_liquidity_ind=last_liquidity_ind

            )
        )

    def add_NewOrdSingleRFQExecutionReport(self, session: str, account: str, ex_destination: str, order_qty: int,
                                           restated_qty: int, new_reply: bool, restated_reply: bool,
                                           reply_delay: int = 0):
        return self.sim.createNewOrdSingleRFQExecutionReport(
            request=TemplateNewOrdSingleRQFRestated(connection_id=ConnectionID(session_alias=session),
                                                    account=account,
                                                    exdestination=ex_destination,
                                                    orderQty=order_qty,
                                                    restatedQty=restated_qty,
                                                    newReply=new_reply,
                                                    RestatedReply=restated_reply,
                                                    reply_delay=reply_delay
                                                    ))

    def add_NewOrdSingle_MarketAuction(self, session: str, account: str, venue: str):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: AtTheOpen, AtTheClose
        by parameters: Account, ExDestination

        Result Message: ExecutionReport PendingNew, ExecutionReport New

        Description: Send 2 execution reports on message 35=D if TIF == AtTheOpen or AtTheClose and OrderType=MKT
        Use cases: Used for RB Market Auction tests.

        Note: Market child orders doesn't executed during the Auction. Because of that default rule for the MarketOrders couldn't be use for the Auction.
        OrderType=MKT
       """
        return self.sim.createNewOrdSingleMarketAuction(
            request=TemplateNewOrdSingleMarketAuction(connection_id=ConnectionID(session_alias=session),
                                                      account=account,
                                                      venue=venue))

    def add_OrderCancelRequestRFQExecutionReport(self, session: str, account: str, ex_destination: str,
                                                 acceptCancel: bool, delay: int = 0):
        """
        Triggered on Message: OrderCancelRequest (TerminateQuoteRequest).
        By parameters: ExDestination.

        Additional input parameters: acceptCancel: bool.

        Result Message: ExecutionReport Cancelled or OrderCancelReject (depends on the acceptCancel parameter).

        Description: Used for answer with the ExecutionReport Cancelled or OrderCancelReject to the TerminateQuoteRequest in the Kepler MPDark tests. It is possible to set up delay for the answer.

        Use cases: Very useful when we need to answer with the ExecutionReport Cancelled or OrderCancelReject to the TerminateQuoteRequest.

        Notes: The answer contains Kepler custom tags.
        """
        return self.sim.createOrderCancelRequestRFQExecutionReport(
            request=TemplateOrderCancelRFQRequest(connection_id=ConnectionID(session_alias=session),
                                                  account=account,
                                                  exdestination=ex_destination,
                                                  acceptCancel=acceptCancel,
                                                  delay=delay
                                                  ))

    def add_NewOrdSingleExecutionReportEliminateFixStandard(self, session: str, account: str, ex_destination: str,
                                                            price: float):
        return self.sim.createNewOrdSingleExecutionReportEliminateFixStandard(
            request=TemplateNewOrdSingleExecutionReportEliminateFixStandard(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=ex_destination,
                price=price
            )
        )

        # ------------------------

    def add_NewOrderSingle_RFQ_Reject(self, session: str, account: str, ex_destination: str, order_qty: int,
                                      reply_delay: int = 0):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: Day.
        By parameters: Account, ExDestination, OrderQty, AlgoCst01.

        Result Message: ExecutionReport Reject.

        Description: Used for answer with the ExecutionReport Reject only to the RFQ NewOrderSingle message in the Kepler MPDark tests. It is possible to set up delay for the answer.

        Use cases: Very useful when we need to answer only with the execution report Reject only to the RFQ NewOrderSingle message.
        """
        return self.sim.createNewOrdSingleRQFRejected(
            request=TemplateNewOrdSingleRQFRejected(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=ex_destination,
                orderQty=order_qty,
                reply_delay=reply_delay
            )
        )

    def add_NewOrdSingle_MarketPreviouslyQuoted(self, session: str, account: str, venue: str, trade: bool,
                                                tradedQty: int, avgPrice: float, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all except FOK.
        By parameters: Account, ExDestination, TimeInForce not equal to 4, OrdType is equal 'D'.

        Additional input parameters: trade: bool.

        Result Message: ExecutionReports PendingNew → New. Then Fill or PartiallFill → Eliminated
        or Eliminated (based on the 'trade' and the 'tradedQty' parameters

        Description: Used for answer to the NewOrderSingle message for Market LIS childs..

        Use cases:
        It can be execution reports PendingNew → New → Trade, if 'trade'=True and 'tradedQty' = OrderQty.

        Or PendingNew → New → Trade → Eliminated, if 'trade'=True and 'tradedQty' < OrderQty.

        Or PendingNew → New → Eliminated if 'trade'=False. It is possible to set up delay for the answer
        """
        return self.sim.createNewOrdSingleMarketPreviouslyQuoted(
            request=TemplateNewOrdSingleMarketPreviouslyQuoted(connection_id=ConnectionID(session_alias=session),
                                                               account=account,
                                                               venue=venue,
                                                               trade=trade,
                                                               tradedQty=tradedQty,
                                                               avgPrice=avgPrice,
                                                               delay=delay))

    def add_OrderCancelReplaceRequestExecutionReportWithTrade(self, session: str, account: str, exdestination: str,
                                                              price: float, cumQtyBeforeReplace: int, tradedQty: int):
        """
        Triggered on Message: OrderCancelReplaceRequest.
        By parameters: Account, ExDestination.

        Result Message: ExecutionReports Replaced → Trade.

        Description: Used for answer only the execution reports Replaced → Trade. to the OrderCancelReplaceRequest message.

        Use cases: Can be used in the inflight cases when the trade should be after the replace.
        """
        return self.sim.createOrderCancelReplaceExecutionReportWithTrade(
            request=TemplateOrderCancelReplaceExecutionReportWithTrade(
                connection_id=ConnectionID(session_alias=session),
                account=account,
                exdestination=exdestination,
                price=price,
                CumQtyBeforeReplace=cumQtyBeforeReplace,
                tradedQty=tradedQty
                ))

    def add_NewOrdSingleExecutionReportTradeByOrdQtyRBCustom(self, session: str, account: str, exdestination: str,
                                                             price: float,
                                                             traded_price: float, qty: int, traded_qty: int,
                                                             delay: int = 0):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: all except IOC, FOK
        by parameters: Account, ExDestination, Price, OrderQty

        Result Message: ExecutionReport  Fill or ExecutionReport  PartialFill
        with params: TradedPrice, TradedQty, RBCustom parameters (tag 8016, 20010-20021)

        Description: Send Execution report Fill on every 35=D  on OrderQty which we determine in TradedQty parameter with RBCustom parameters (tag 20010-20021) if TIF != IOC or FOK
        Use cases: used for the REDBURN case

       """
        return self.sim.createNewOrdSingleExecutionReportTradeByOrdQtyRBCustom(
            request=TemplateNewOrdSingleExecutionReportTradeByOrdQtyRBCustom(connection_id=ConnectionID(session_alias=session),
                                                                     account=account,
                                                                     exdestination=exdestination,
                                                                     price=price,
                                                                     traded_price=traded_price,
                                                                     qty=qty,
                                                                     traded_qty=traded_qty,
                                                                     delay=delay))

    def add_NewOrdSingle_IOCTradeOnFullQty(self, session: str, account: str, venue: str, trade: bool, price: float, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: IOC.
        By parameters: Account, ExDestination, Price.

        Additional input parameters: trade: bool.

        Result Message: ExecutionReport PendingNew,  ExecutionReport New and ExecutionReport Trade or ExecutionReport Eliminated based on the 'trade' parameter.

        Description: Differ from the add_NewOrdSingle_IOC  in that the no need to set up the TradedQty. All childs which parameter are equal to the trigger parameters will be fullfilled. It is possible to set up delay for the answer.

        Use cases: used in the Kepler tests when the child order can be randomly created on the on the one of the venues for the each test run to prevent Overfill.
        """
        return self.sim.createNewOrdSingleIOCTradeOnFullQty(
            request=TemplateNewOrdSingleIOCTradeOnFullQty(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            price=price,
                                            delay=delay))

    def add_NewOrderSingle_ExecutionReport_DoneForDay(self, session: str, account: str, ex_destination: str,
                                                     price: float, delay: int = 0, text: str = "DoneForDay"):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: all.
        By parameters: Account, ExDestination, Price.

        Additional input parameters: Text.

        Result Message: ExecutionReport DoneForDay (39=3, 150=3).

        Description: Used for answer with the ExecutionReport DoneForDay in the Kepler tests. It is possible to set up delay for the answer and the text.

        Use cases: Very useful when we need to answer with the ExecutionReport DoneForDay in the Kepler tests.

        Notes: Should be used with the add_NewOrdSingleExecutionReportPendingAndNew rule.
        """
        return self.sim.createNewOrdSingleExecutionReportDoneForDay(
            request=TemplateNewOrdSingleExecutionReportDoneForDay(connection_id=ConnectionID(session_alias=session),
                                             account=account,
                                             exdestination=ex_destination,
                                             price=price,
                                             delay=delay,
                                             text=text))

    def add_NewOrdSingle_IOCTradeByOrderQty(self, session: str, account: str, venue: str, trade: bool, price: float, traded_price: float, qty: int, traded_qty: int, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle.
        Supported TimeInForce: IOC.
        By parameters: Account, ExDestination, Price, OrderQty.

        Additional input parameters: trade: bool, traded_qty, traded_price.

        Result Message: ExecutionReport PendingNew, ExecutionReport New -> ExecutionReport Fill or PartiallFill → Eliminated or Eliminated (based on the 'trade' and the 'tradedQty' parameters.

        Description: Differ from the add_NewOrdSingle_IOC  in that the it possible to set up defined qty, traded_qty, price and traded_price. It is possible to set up delay for the answer.

        Use cases:  used in the Kepler tests when it needs to fill or eliminate not all child on the defined venue.
        """
        return self.sim.createNewOrdSingleIOCTradeByOrderQty(
            request=TemplateNewOrdSingleIOCTradeByOrderQty(connection_id=ConnectionID(session_alias=session),
                                            account=account,
                                            venue=venue,
                                            trade=trade,
                                            price=price,
                                            traded_price=traded_price,
                                            qty=qty,
                                            traded_qty=traded_qty,
                                            delay=delay
                                            ))

    def add_NewOrdSingleExecutionReportTradeOnFullQty(self, session: str, account: str, venue: str, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: all except IOC, FOK
        by parameters: Account, ExDestination

        Result Message: ExecutionReport Trade

        Description: Answer with ER Trade on the NewOrderSingle with any TIF exclude IOC and FOK without price or order type  restriction.

        Use cases: Very useful when we need to trade many orders on. We don't need to create many rules with the price restriction
       """
        return self.sim.createNewOrdSingleTradeOnFullQty(
            request=TemplateNewOrdSingleTradeOnFullQty(connection_id=ConnectionID(session_alias=session),
                                                             account=account,
                                                             venue=venue,
                                                             delay=delay))

    def add_NewOrdSingleExecutionReportAll(self, session: str, account: str, venue: str, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: all except IOC, FOK
        by parameters: Account, ExDestination

        Result Message: ExecutionReport PendingNew, ExecutionReport New

        Description: Answer with ER PendingNew/New on the NewOrderSingle with any TIF exclude IOC and FOK without price or order type  restriction.

        Use cases: Very useful when we need to check many orders on which we both ER. We don't need to create many rules with the  price restriction

        Note: OrderType= LMT or MKT
        Also have add_NewOrdSingleExecutionReportPendingAndNew, but it contains restrictions
       """
        return self.sim.createNewOrdSingleExecutionReportAll(
            request=TemplateNewOrdSingleExecutionReportAll(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       venue=venue,
                                                       delay=delay))

    def add_NewOrdSingleExecutionReportIOCAll(self, session: str, account: str, venue: str, delay: int = 0):
        """
        Triggered on Message: NewOrdSingle
        supported TimeInForce: IOC
        by parameters: Account, ExDestination,

        Result Message: ExecutionReport PendingNew, ExecutionReport New

        Description: Answer with ER PendingNew/New on the NewOrderSingle with TIF = IOC without price or order type restriction.

        Use cases: Very useful when we need to check many IOC orders on which we both ER. We don't need to create many rules with the  price restriction

        Note: OrderType= LMT or MKT
        Also have add_NewOrdSingle_IOC, but it contains restrictions
       """
        return self.sim.createNewOrdSingleExecutionReportIOCAll(
            request=TemplateNewOrdSingleExecutionReportIOCAll(connection_id=ConnectionID(session_alias=session),
                                                       account=account,
                                                       venue=venue,
                                                       delay=delay))

    def add_MarketDataRequestWithTimeout(self, session: str, symbols: list):
        return self.sim.createMarketDataRequestWithTimeout(
            request=TemplateMarketDataRequestWithTimeout(connection_id=ConnectionID(session_alias=session),
                                            symbols=symbols
                                            ))



if __name__ == '__main__':
    # rule_manager = RuleManager()
    # rule_manager.print_active_rules()
    # rule_manager.remove_all_rules()
    rule_manager_eq = RuleManager(Simulators.equity)
    print("_________________________")
    rule_manager_eq.remove_all_rules()
    rule_manager_eq.print_active_rules()
    Stubs.factory.close()

