import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8342(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.client2 = self.data_set.get_client_by_name("client_pos_3")
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.order_book.set_filter(filter_list).check_order_fields_list({OrderBookColumns.washbook.value:
                                                                             self.wash_book})
        # endregion
        # region Step 2
        self.order_ticket.set_order_details(client=self.client2)
        self.order_ticket.re_order()
        self.order_book.check_order_fields_list({OrderBookColumns.washbook.value: self.wash_book},
                                                verification_method=VerificationMethod.NOT_EQUALS)
        # endregion
