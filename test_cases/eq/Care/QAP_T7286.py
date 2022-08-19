import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Suspended, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7286(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.session_id2 = set_session_id(self.fe_env.target_server_win)
        self.fun_config = self.fe_env.folder + "\ConfigFiles\Default\\functional.config"
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id2)
        self.base_main_window = BaseMainWindow(self.test_id, self.session_id2)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id2)
        self.new_price = '50'
        self.new_qty = '200'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        tree = ET.parse(self.fun_config)
        root = tree.getroot()
        root.find("tradingOptions/orderSuspendOrRelease").set("enable", "true")
        tree.write(self.fun_config)
        self.base_main_window.open_fe(self.report_id, self.fe_env, 2, False)

        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        # endregion
        # region Step 1
        self.order_book.suspend_order(filter_dict=filter_dict)
        self.order_book.refresh_order(filter_list=filter_list)
        # endregion
        # region Step 2,3
        self.order_ticket.set_order_details(qty=self.new_qty, limit=self.new_price)
        self.order_ticket.amend_order(filter_list)
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list(
            {OrderBookColumns.qty.value: self.new_qty, OrderBookColumns.limit_price.value: self.new_price,
             OrderBookColumns.suspend.value: Suspended.yes.value})
        # endregion
        # region Step 4
        self.order_book.release_order(filter_list=filter_list)
        self.order_book.refresh_order(filter_list=filter_list)
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list({OrderBookColumns.suspend.value: Suspended.no.value})
        # endregion
        # region Step 5
        self.order_book.manual_execution(qty=str(int(int(self.new_qty) / 2)), filter_dict=filter_dict)
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region Step 6
        self.order_book.suspend_order(filter_dict=filter_dict)
        self.order_book.refresh_order(filter_list=filter_list)
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list({OrderBookColumns.suspend.value: Suspended.yes.value})
        # endregion
        # region Step 7
        self.order_ticket.set_order_details(error_expected=True)
        footer = self.order_ticket.split_order(filter_list=filter_list)
        self.order_book.compare_values({
            "ErrorMessage": f'Error - [QUOD-11801] Validation by CS failed, Request not allowed:  The order is suspended, OrdID={order_id}'},
            footer,
            "Check error in Slit Ticket")
        # endregion
        # region Step 8
        self.order_book.cancel_order(filter_list=filter_list)
        self.order_book.set_filter(filter_list)
        self.order_book.check_order_fields_list(
            {OrderBookColumns.suspend.value: Suspended.yes.value, OrderBookColumns.sts.value: ExecSts.cancelled.value})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.base_main_window.close_fe()
        tree = ET.parse(self.fun_config)
        root = tree.getroot()
        root.find("tradingOptions/orderSuspendOrRelease").set("enable", "false")
        tree.write(self.fun_config)
