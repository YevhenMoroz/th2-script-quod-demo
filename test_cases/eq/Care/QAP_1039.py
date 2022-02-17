import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Connectivity
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts, OrderBookColumns, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_1039(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty2 = "1000"
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.username = Stubs.custom_config['qf_trading_fe_user']
        self.password = Stubs.custom_config['qf_trading_fe_password']
        self.fix_manager = FixManager(self.ss_connectivity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.order_inbox.accept_order('O', 'M', 'S')
        # endregion
        # region manual execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).manual_execution()
        # endregion
        # region check exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # region
        # region amend values
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        self.order_ticket.set_order_details(qty=self.qty2)
        self.order_ticket.amend_order()
        # endregion
        # region check qty2 and price2
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.qty.value: self.qty2, OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # region
        # region complete order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).complete_order()
        # endregion
        # region check exec status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        # endregion


