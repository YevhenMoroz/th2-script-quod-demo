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
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TimeInForce, OrderType, \
    TradeBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_5951(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        # self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.no_allocs = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        self.fix_message.change_parameters({"Accounts": self.client, "PreAllocGrp": self.no_allocs})
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.client_id = self.fix_message.get_parameter('ClOrdID')
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.rule_manager = RuleManager(sim=Simulators.equity)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create dma orders
        order_id1 = self.__send_fix_orders('1')
        # order_id1 = self.response[0].get_parameter("OrderID")
        order_id2 =self.__send_fix_orders('2')
        # order_id2 = self.response[0].get_parameter("OrderID")
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.client_id]).mass_book([1, 2])
        self.__verify_fees_in_exec(self.trades, order_id1)
        self.__verify_fees_in_exec(self.trades, order_id2)
        self.__verify_fees_in_middle_office(self.mid_office, order_id1)
        self.__verify_fees_in_middle_office(self.mid_office, order_id2)

    def __send_fix_orders(self, side:str):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.fix_env.buy_side, self.client_for_rule, self.mic, float(self.price), float(self.price), int(self.qty),
                int(self.qty), 1)
            self.fix_message.change_parameters({'Side': side})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rules([nos_rule, trade_rule])
        return order_id

    def __verify_fees_in_exec(self, trades: OMSTradesBook, order_id:str):
        trades.set_filter([OrderBookColumns.order_id.value, order_id])
        commissions = {
            TradeBookColumns.client_commission.value: trades.extract_field(TradeBookColumns.client_commission.value)}
        fees = {TradeBookColumns.exec_fees.value: trades.extract_field(TradeBookColumns.exec_fees.value)}
        trades.compare_values({TradeBookColumns.client_commission.value: "1.123"}, commissions,
                              event_name='Check values')
        trades.compare_values({TradeBookColumns.exec_fees.value: "1.123"}, fees, event_name='Check values')

    @staticmethod
    def __verify_fees_in_middle_office(middle_office: OMSMiddleOffice, order_id:str):
        commissions = middle_office.extract_block_field(MiddleOfficeColumns.client_comm.value, row_number=1, filter_list=[MiddleOfficeColumns.order_id.value, order_id])
        fees = middle_office.extract_block_field(MiddleOfficeColumns.total_fees.value, row_number=1, filter_list=[MiddleOfficeColumns.order_id.value, order_id])
        middle_office.compare_values({MiddleOfficeColumns.client_comm.value: "1.123"}, commissions,
                                     event_name='Check values')
        middle_office.compare_values({MiddleOfficeColumns.total_fees.value: "1.123"}, fees, event_name='Check values')
