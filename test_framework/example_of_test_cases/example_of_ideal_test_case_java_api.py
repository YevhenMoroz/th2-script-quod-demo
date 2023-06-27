from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns

# region TestData
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
qty = "100"
price = "10"
# endregion


class QAP_Example(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_connectivity = None
        self.ja_manager = None
        self.base_window = None
        self.ord_book = None
        self.cl_inbox = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Initialization
        self.ja_connectivity = SessionAliasOMS().ja_connectivity
        self.ja_manager = JavaApiManager(self.ja_connectivity, bca.create_event(Path(__file__).name[:-3],
                                                                                self.report_id))
        self.base_window = BaseMainWindow(self.test_id, self.session_id)
        self.ord_book = OMSOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        # endregion
        # region Variables
        venue = self.data_set.get_venue_by_name("venue_1")
        # endregion
        # region Open FE
        self.base_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send Care Order via Java Api
        ord_submit = OrderSubmitOMS(self.data_set).set_default_care_limit()
        self.ja_manager.send_message(ord_submit)
        # endregion
        # region Accept Care
        self.cl_inbox.accept_order(venue, qty, price)
        # endregion
        # region Trade Order via Java Api
        ord_id = self.ord_book.extract_field("Order ID")
        trd_entry = TradeEntryOMS(self.data_set).set_default_trade(ord_id)
        self.ja_manager.send_message(trd_entry)
        # endregion
        # region Verify that order filled
        self.ord_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion