import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Suspended, SecondLevelTabs, MatchWindowsColumns, TradeBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7291(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.qty_dma = "40"
        self.price_dma = "10"
        self.fix_message_dma.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty_dma}, "Price": self.price_dma})
        self.fix_message_care = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty_care = "50"
        self.price_care = "20"
        self.fix_message_care.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty_care}, "Price": self.price_care})
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.fix_manager = FixManager(self.ss_connectivity, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.trade_book = OMSTradesBook(self.case_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send DMa order and execute it
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price_dma), float(self.price_dma),
                                                                         int(self.qty_dma), int(self.qty_dma), 1)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_dma)
            order_id_dma = response[0].get_parameter("OrderID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        exec_order_dma_id = self.order_book.set_filter(
            [OrderBookColumns.order_id.value, order_id_dma]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, ["ExecID"], [1])[0]['ExecID']
        print(exec_order_dma_id)
        # endregion
        # region create Care order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_care)
        order_id_care = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region suspend order
        self.order_book.suspend_order(filter_dict={OrderBookColumns.order_id.value: order_id_care})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_care]).check_order_fields_list(
            {OrderBookColumns.suspend.value: Suspended.yes.value})
        # endregion
        # region manual match
        error = self.trade_book.manual_match(self.qty_dma, [MatchWindowsColumns.order_id.value, order_id_care],
                                             [TradeBookColumns.exec_id.value, exec_order_dma_id], error_expected=True)
        print(error)
        self.trade_book.compare_values(
            {'Match Window Error': f"Error - [QUOD-16533] Request not allowed:  The order is suspended, OrdID={order_id_care}"},
            error, "Check error in Manual Match Ticket")
        # endregion
