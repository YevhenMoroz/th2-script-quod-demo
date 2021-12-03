import logging
import os

from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import FixMessageOrderCancelReplaceRequestOMS
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP4648(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_4648(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        main_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        lokup = "VETO"
        qty = "100"
        price = "20"
        new_price = "1"
        # endregion
        # region Open FE
        main_window.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS().set_default_order_list()
        fix_manager.send_message_and_receive_response_fix_standard(nol)
        # endregion
        # region Set-up parameters for ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(nol)
        # endregion
        # region Check ListStatus
        fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        cl_inbox.accept_order(lokup, qty, price)
        cl_inbox.accept_order(lokup, qty, price)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS().set_default_new_list(nol)
        exec_report2 = FixMessageExecutionReportOMS().set_default_new_list(nol, 1)
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report1)
        fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region Send OrderCancelReplaceRequest

        rep_req = FixMessageOrderCancelReplaceRequestOMS().set_default(nol).change_parameters({'Price': new_price})
        fix_manager.send_message_and_receive_response_fix_standard(rep_req)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report3 = FixMessageExecutionReportOMS().set_default_replaced_list(nol).change_parameters({'Price': new_price})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report3, key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4648()


