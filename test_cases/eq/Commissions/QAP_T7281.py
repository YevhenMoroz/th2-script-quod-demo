import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, TradeBookColumns, SecondLevelTabs, \
    ExecType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7281(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             "ExDestination": self.data_set.get_mic_by_name("mic_2"),
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message()
        self.rest_commission_sender.send_post_request()
        # endregion
        # region create order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        # endregion
        # region verify commission
        trade_comm = self.order_book.extract_sub_lvl_fields([TradeBookColumns.client_commission.value],
                                                            [SecondLevelTabs.executions.value],
                                                            {OrderBookColumns.order_id.value: order_id},
                                                            [{TradeBookColumns.exec_type.value: ExecType.trade.value}])
        self.order_book.compare_values({TradeBookColumns.client_commission.value: "0.01"}, trade_comm,
                                       "Verify Trade commissions")
        calculate_comm = self.order_book.extract_sub_lvl_fields([TradeBookColumns.client_commission.value],
                                                                [SecondLevelTabs.executions.value],
                                                                {OrderBookColumns.order_id.value: order_id},
                                                                [{
                                                                     TradeBookColumns.exec_type.value: ExecType.calculated.value}])
        self.order_book.compare_values({TradeBookColumns.client_commission.value: "0.01"}, calculate_comm,
                                       "Verify Calculated commissions")
        self.mid_office.set_modify_ticket_details(extract_book=True)
        extract_book = self.mid_office.book_order([OrderBookColumns.order_id.value, order_id])
        actual_values = {'Commissions': extract_book.get('book.totalComm')}
        expected_values = {'Commissions': "0.01"}
        self.order_book.compare_values(expected_values, actual_values,
                                       "Verify Book commissions")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_orders(self):
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
