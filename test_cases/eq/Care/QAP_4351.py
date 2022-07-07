import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from custom.verifier import Verifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_4351(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)



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
        result = self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution()
        verifier = Verifier(self.test_id)
        verifier.set_event_name("Check value")
        verifier.compare_values("Order ID from View",
                                result['Trade Ticket Error'],"Error - [QUOD-11503] Invalid status [SuspendedCare=Y]")
        verifier.verify()
#
# def execute(report_id, session_id):
#     case_name = "QAP-4351"
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
#
#     # region Create CO
#     fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
#     eq_wrappers.accept_order('VETO', qty, price)
#     # order_id = eq_wrappers.get_order_id(base_request)
#     # endregion
#
#     # region suspend order
#     eq_wrappers.suspend_order(base_request, False)
#     # endregion
#     result = eq_wrappers.manual_execution(base_request, qty, price, True)
#     verifier = Verifier(case_id)
#     verifier.set_event_name("Check value")
#     verifier.compare_values("Order ID from View",
#                             "Error - [QUOD-11503] Invalid status [SuspendedCare=Y]",
#                             result['Trade Ticket Error'],
#                             )
#     verifier.verify()
