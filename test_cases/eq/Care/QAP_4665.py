import logging
import os

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_4665(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_4665(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        ord_book = OMSOrderBook(self.case_id, self.session_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderSingle
        param = {"Account": "CLIENT_FIX_CARE"}
        nos = FixMessageNewOrderSingleOMS().set_default_care_limit(Instrument.DUMMY).change_parameters(param)
        ord_book.scroll_order_book()
        fix_manager.send_message_fix_standard(nos)
        # endregion
        # region Check value
        exp_val = {"Security Id": "UNKNOWN", "Symbol": "UNKNOWN", "Lookup": "UNKNOWN"}
        # ord_book.scroll_order_book()
        act_val = ord_book.extract_fields_list(exp_val)
        ord_book.compare_values(exp_val, act_val, "Check UNKNOWN Instrument")
        # endregion

    # @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4665()
