import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, OrderBookColumns, ExecPcy
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7559(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.btn_name = "Button" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.qty_to_perc = "50"
        self.route = self.data_set.get_route('route_2')
        self.strategy = "MS TWAP(ASIA)"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        self.order_book.create_quick_button(self.btn_name, self.qty_to_perc, "Split", order_type=OrderType.limit.value)
        # endregion
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        # endregion
        # region use quick button
        self.order_book.click_quick_button(self.btn_name, order_id)
        # endregion
        # region check child order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list(
            {OrderBookColumns.exec_pcy.value: ExecPcy.dma.value, OrderBookColumns.qty.value: str(int(int(self.qty)/2))})
        # endregion