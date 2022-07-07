import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request, call
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest

from test_framework.old_wrappers import eq_wrappers
from custom.basic_custom_actions import create_event

from test_framework.old_wrappers.eq_wrappers import open_fe


from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@try_except(test_id=Path(__file__).name[:-3])
class QAP_4352(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.base_request = get_base_request(self.session_id, self.test_id)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        self.order_book.suspend_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.suspend.value: "Yes"})
        # endregion
        self.order_ticket.split_order()
        result = self.order_ticket.extract_order_ticket_errors()
        print(result)
        self.order_book.compare_values({"Trade Ticket Error": 'Error - [QUOD-11801] Validation by CS failed '}, result, "Check value")

# #
# def execute(report_id, session_id):
#     case_name = "QAP-4352"
#     # region Declarations
#     qty = "40"
#     price = "11"
#     client = "CLIENT_FIX_CARE"
#     case_id = create_event(case_name, report_id)
#     base_request = get_base_request(session_id, case_id)
#     work_dir = Stubs.custom_config['qf_trading_fe_folder']
#     username = Stubs.custom_config['qf_trading_fe_user']
#     password = Stubs.custom_config['qf_trading_fe_password']
#     # endregion
#
#     # region Open FE
#     open_fe(session_id, report_id, case_id, work_dir, username)
#     # endregion
#     # region Create CO
#     eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
#     eq_wrappers.accept_order('VETO', qty, price)
#     order_id = eq_wrappers.get_order_id(base_request)
#     # endregion
#
#     # region suspend order
#     eq_wrappers.suspend_order(base_request, False)
#     # endregion
#     eq_wrappers.split_order(base_request, qty, 'Limit', price)
#     result = eq_wrappers.extract_error_order_ticket(base_request)
#     verifier = Verifier(case_id)
#     verifier.set_event_name("Check value")
#     verifier.compare_values("Order ID from View",
#                             "Error - [QUOD-11801] Validation by CS failed, Request not allowed:  The order is "
#                             "suspended, OrdID=" + order_id,
#                             result['ErrorMessage'],
#                             )
#     verifier.verify()
