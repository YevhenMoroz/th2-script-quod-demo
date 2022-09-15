import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns, \
    PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7393(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.oms_basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        self.fix_manager.send_message_fix_standard(self.fix_message)
        first_order_id = self.order_book.extract_field(OrderBookColumns.order_id.value, row_number=1)
        second_order_id = self.order_book.extract_field(OrderBookColumns.order_id.value, row_number=2)
        basket_id = self.oms_basket_book.get_basket_value(BasketBookColumns.id.value)
        # endregion
        # region accept orders
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region check basket status
        self.oms_basket_book.check_basket_field(BasketBookColumns.status.value, BasketBookColumns.exec_sts.value)
        # endregion
        # region complete order
        self.oms_basket_book.complete_basket(filter_dict={BasketBookColumns.id.value: basket_id})
        # endregion
        # region check complete basket
        self.order_book.set_filter([OrderBookColumns.order_id.value, first_order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
             OrderBookColumns.done_for_day.value: "Yes"})
        self.order_book.set_filter([OrderBookColumns.order_id.value, second_order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
             OrderBookColumns.done_for_day.value: "Yes"})
        # endregion
        # region uncomplete basket
        self.oms_basket_book.un_complete(filter_dict={BasketBookColumns.id.value: basket_id})
        # endregion
        # region check uncomplete basket
        self.order_book.set_filter([OrderBookColumns.order_id.value, first_order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: "",
             OrderBookColumns.done_for_day.value: ""})
        self.order_book.set_filter([OrderBookColumns.order_id.value, second_order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: "",
             OrderBookColumns.done_for_day.value: ""})
        # endregion

