import logging
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7369(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_1")
        self.qty=self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_2")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name("currency_3")
        self.change_params = {'Account': self.client,
                              "Currency": self.cur,
                              'ExDestination': self.mic,
                              'PreAllocGrp': {
                                  'NoAllocs': [{
                                      'AllocAccount': self.account,
                                      'AllocQty': "100"}]}}
        self.client_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.ord_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.fix_verifier_bs = FixVerifier(self.fix_env.drop_copy, self.test_id)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create Care order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        # endregion
        # region Accept order
        self.client_inbox.accept_order()
        # endregion
        # region Split
        nos_rule=None
        trade_rule=None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule, self.mic,
                                                                                             int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.client_for_rule, self.mic, int(self.price),
                                                                                       int(self.qty), 2)
            self.ord_ticket.split_order([OrderBookColumns.cl_ord_id.value, self.client_id])

        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

        parties = {
            'NoPartyIDs': [
                {'PartyRole': "36",
                 'PartyRoleQualifier': '1011',
                 'PartyID': "gtwquod4",
                 'PartyIDSource': "D"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart_SA1",
                 'PartyIDSource': "C"}

            ]
        }
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new(self.fix_message).change_parameters(
            {"Parties": parties, "Currency": "GBp"})
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"Parties": parties, "ReplyReceivedTime": "*", "SecondaryOrderID": "*", "LastMkt": "*", "Currency": "GBp",
             "Account": self.account})
        exec_report2.remove_parameter("SettlCurrency")
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region unmatch and transfer
        self.order_book.unmatch_and_transfer("Facilitation", {OrderBookColumns.cl_ord_id.value: self.client_id})
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.client_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: self.qty, OrderBookColumns.exec_sts.value: ""})
        self.__check_exec_tab(OrderBookColumns.qty.value, '0', 1, {OrderBookColumns.cl_ord_id.value: self.client_id})
        self.__check_exec_tab(OrderBookColumns.unmatched_qty.value, '0', 1, {OrderBookColumns.cl_ord_id.value: self.client_id})
        self.__check_exec_tab(OrderBookColumns.exec_price.value, '0', 1, {OrderBookColumns.cl_ord_id.value: self.client_id})
        # endregion
        # region Set-up parameters for ExecutionReports
        parties = {
            'NoPartyIDs': [
                {'PartyRole': "36",
                 'PartyRoleQualifier': '1011',
                 'PartyID': "gtwquod4",
                 'PartyIDSource': "D"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart_SA1",
                 'PartyIDSource': "C"}

            ]
        }
        noparties = {
            'NoParty': [
                {'PartyRole': "36",
                 'PartyID': "gtwquod4",
                 'PartyIDSource': "D"},
                {'PartyRole': "66",
                 'PartyID': "MarketMaker - TH2Route",
                 'PartyIDSource': "C"},
                {'PartyRole': "67",
                 'PartyID': "InvestmentFirm - ClCounterpart_SA1",
                 'PartyIDSource': "C"}

            ]
        }
        all_param = {'NoAllocs': [{
                                      'AllocAccount': self.account,
                                      'AllocQty': "100",
                                        "AllocAcctIDSource": '*'}]}
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message).change_parameters(
            {"Parties": parties, 'ReplyReceivedTime':"*", "Account": self.account,"Currency": "GBp", "LastMkt": self.mic})
        exec_report1.remove_parameter("SettlCurrency")
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(
            self.fix_message).change_parameters(
            {"NoParty": noparties,  "Account": self.client, "Currency": "GBp", 'QuodTradeQualifier':'*',
             "LastMkt": self.mic, "BookID": "*", "tag5120":"*", "ExecBroker": "*", "M_PreAllocGrp": all_param})
        exec_report2.remove_parameters(['TradeReportingIndicator',  "SettlCurrency", "Parties"])
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.fix_verifier_bs.check_fix_message_fix_standard(exec_report2)
        # endregion

    def __check_exec_tab(self, field:str, expect:str, row:int, filtr:dict = None):
        acc_res = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                        [field], [row],
                                                        filtr)
        self.order_book.compare_values({field: expect}, {field: acc_res[0][field]}, "Check Execution tab")

