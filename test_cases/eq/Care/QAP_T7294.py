import logging
import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, MenuItemFromOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7294(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.cl_ord_id = self.fix_message.get_parameter("ClOrdID")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region split first order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            self.order_ticket.set_order_details(qty=str(int(int(self.qty) + 1)))
            self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id])
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region check values
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.qty.value: self.qty, OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region check context menu
        split = self.order_book.is_menu_item_present(MenuItemFromOrderBook.split.value, [1],
                                                     filter_dict={OrderBookColumns.order_id.value: order_id})
        split_limit = self.order_book.is_menu_item_present(MenuItemFromOrderBook.split_limit.value, [1],
                                                           filter_dict={OrderBookColumns.order_id.value: order_id})
        self.order_book.compare_values({'Split': 'false', "Split Limit": 'false'}, {'Split': split, "Split Limit": split_limit},
                                       f'Verifying, that {MenuItemFromOrderBook.split.value} and  {MenuItemFromOrderBook.split_limit.value}'
                                       f'don`t present at menu item')
        # endregion
