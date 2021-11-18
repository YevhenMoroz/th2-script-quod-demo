import logging
import os

from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.TestCase import TestCase
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.SessionAlias import SessionAliasOMS
from quod_qa.wrapper_test.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from quod_qa.wrapper_test.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from quod_qa.wrapper_test.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS

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
        fix_verifier = FixVerifier(self.ss_connectivity, self.report_id)
        cl_inbox = OMSClientInbox(self.case_id,self.session_id)
        # endregion
        cl_inbox.open_fe(self.session_id)
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
        # region Set-up parameters for ExecutionReports
        exec_reprt1 = FixMessageExecutionReportOMS().change_parameters({'Account': "CLIENT_FIX_CARE", "OrderQty": "100",
                                                                        "Instrument":DataSet.Instrument.FR0004186856,
                                                                        'ClOrdID':cl_ord_id1})
        exec_reprt2 = FixMessageExecutionReportOMS().change_parameters({'Account': "CLIENT_FIX_CARE", "OrderQty": "100",
                                                                        "Instrument": DataSet.Instrument.FR0004186856,
                                                                        'ClOrdID': cl_ord_id2})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_reprt1)
        fix_verifier.check_fix_message_fix_standard(exec_reprt2)
        # endregion

    # @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_4648()
