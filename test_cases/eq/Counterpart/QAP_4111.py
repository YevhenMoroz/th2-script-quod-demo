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
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_4111(TestCase):
    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.test_id)
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity
        self.dc_connectivity = SessionAliasOMS().dc_connectivity

    def qap_4111(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.report_id)
        cln_inbox = OMSClientInbox(self.case_id, self.session_id)
        ord_book = OMSOrderBook(self.case_id, self.session_id)
        main_win = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        client = "CLIENT_COUNTERPART"
        # endregion
        # region open FE
        main_win.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Create care order
        change_params = {'Account': client}
        nos = FixMessageNewOrderSingleOMS().set_default_care_limit(Instrument.FR0004186856).change_parameters(
            change_params)
        response = fix_manager.send_message_and_receive_response_fix_standard(nos)
        cln_inbox.accept_order("VETO", response[0].get_parameters()['LeavesQty'], response[0].get_parameters()['Price'])
        ord_book.scroll_order_book()
        # endregion
        # region Execute and complete
        ord_book.manual_execution(execution_firm="ExecutingFirm", contra_firm="ContraFirm")
        ord_book.complete_order()
        # endregion
        # region Check ExecutionReports
        act_exec_firm = ord_book.extract_2lvl_fields("Executions", ["Executing Firm"], [1])
        act_contr_firm = ord_book.extract_2lvl_fields("Executions", ["Contra Firm"], [1])
        ord_book.compare_values({"Executing Firm": "ExecutingFirm"}, act_exec_firm[0], "Executing Firm for ord1")
        ord_book.compare_values({"Contra Firm": "ContraFirm"}, act_contr_firm[0], "Contra Firm for ord1")
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4111()
