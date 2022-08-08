import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7405(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_manager.send_message_fix_standard(nol)
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        order_id = self.order_book.set_filter([OrderBookColumns.basket_id.value, basket_id]).extract_field(
            OrderBookColumns.order_id.value, 2)
        # endregion
        # region Set-up parameters for ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(nol)
        # endregion
        # region Check ListStatus
        self.fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region remove order from basket
        self.basket_book.remove_from_basket({BasketBookColumns.id.value: basket_id}, [1])
        # endregion
        # region check values
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.basket_name.value: "",
             OrderBookColumns.basket_id.value: ""})
        # endregion
