import logging
import os

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.base_window import decorator_try_except
from quod_qa.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from quod_qa.wrapper_test.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP3882(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_3882(self):
        # region Declaration
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        basket_book = OMSBasketOrderBook(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        lokup = "VETO"
        qty = "100"
        price = "20"
        # endregion
        # region Open FE
        cl_inbox.open_fe(self.report_id, work_dir, username, password)
        # endregion
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS().set_default_order_list()
        fix_manager.send_message_and_receive_response_fix_standard(nol)
        # endregion
        # region Set-up parameters for ListStatus
        cl_ord_id1 = nol.get_parameters()['ListOrdGrp']['NoOrders'][0]['ClOrdID']
        cl_ord_id2 = nol.get_parameters()['ListOrdGrp']['NoOrders'][1]['ClOrdID']
        list_id = nol.get_parameters()['ListID']
        list_status = FixMessageListStatusOMS().change_parameters({'ListID': list_id})
        list_status.set_no_orders(0, cl_ord_id1)
        list_status.set_no_orders(1, cl_ord_id2)
        # endregion
        # region Check ListStatus
        fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        cl_inbox.accept_order(lokup, qty, price)
        cl_inbox.accept_order(lokup, qty, price)
        # endregion
        # region cancel Basket
        basket_book.cancel_basket()
        # endregion
        # region Set-up parameters for ExecutionReports
        change_parameters = {
            'Account': "CLIENT_FIX_CARE",
            'HandlInst': '3'
        }
        exec_report1 = FixMessageExecutionReportOMS().set_default_canceled().change_parameters(change_parameters). \
            change_parameters({'ClOrdID': cl_ord_id1})
        exec_report2 = FixMessageExecutionReportOMS().set_default_canceled().change_parameters(change_parameters). \
            change_parameters({'ClOrdID': cl_ord_id2, 'Side': "2"})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report1)
        fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_3882()
