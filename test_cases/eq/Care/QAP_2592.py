import logging
from custom import basic_custom_actions as bca
from pathlib import Path
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom.verifier import Verifier
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import  OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.fix_wrappers.FixManager import FixManager

from stubs import Stubs
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

class QAP_2592(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.rule_manager = RuleManager()
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.base_request = get_base_request(self.session_id, self.test_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region split order
        self.order_ticket.set_order_details(qty=str(int(self.qty)+10))
        self.order_ticket.split_order()
        # endregion
        # region check child qty
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_second_lvl_fields_list({OrderBookColumns.qty.value: self.qty})
        # endregion
        # region set up 0
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region split order
        self.order_ticket.set_order_details(qty="0")
        self.order_ticket.split_order()
        # endregion
        extract_errors_request = ExtractOrderTicketErrorsRequest(self.base_request)
        extract_errors_request.extract_error_message()
        result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
        verifier = Verifier(self.test_id)
        verifier.set_event_name("Check value")
        verifier.compare_values("Order ID from View",
                                'Quantity cannot be negative or null', result['ErrorMessage']
                                )
        verifier.verify()


