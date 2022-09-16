import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8254(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.order_book.mark_reviewed(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "Yes"})
        # endregion
        # region Step 2
        self.order_book.mark_unreviewed(filter_list)
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.reviewed.value: "No"})
        # endregion
