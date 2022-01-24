import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
# region TestData
ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
lokup = "VETO"
qty = "100"
price = "20"
client = "MOClient"
alloc_acc = "test"


# endregion

class QAP_6375(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        fix_manager = FixManager(ss_connectivity, self.test_id)
        cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        ord_book = OMSOrderBook(self.test_id, self.session_id)
        main_window = BaseMainWindow(self.test_id, self.session_id)
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderSingle
        change_params = {'Account': client, 'PreAllocGrp': {
            'NoAllocs': [{
                'AllocAccount': alloc_acc,
                'AllocQty': "100"}]}}
        nol = FixMessageNewOrderSingleOMS().set_default_care_limit().change_parameters(change_params)
        fix_manager.send_message_and_receive_response_fix_standard(nol)
        # endregion
        # region Accept orders
        cl_inbox.accept_order(lokup, qty, price)
        # endregion
        # region Verify
        act_value = ord_book.extract_2lvl_fields("Pre Trade Allocations", ["Id"], [1])
        ord_book.compare_values({"Id": alloc_acc}, act_value[0], "Check Pre Trade Allocation")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
