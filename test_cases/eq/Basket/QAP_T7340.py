import os
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7340(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.ord_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.new_price = "456"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.message)
        cl_ord_id1 = response[0].get_parameters()['OrdListStatGrp']['NoOrders'][0]['ClOrdID']
        # endregion

        # region Check ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(self.message)
        self.fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion

        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message, 1)
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion

        # region Send OrderCancelReplaceRequest
        self.ord_message.change_parameter('ClOrdID', cl_ord_id1)
        rep_req = FixMessageOrderCancelReplaceRequestOMS(self.data_set).set_default(self.ord_message)
        rep_req.change_parameter('Price', self.new_price)
        self.fix_manager.send_message_and_receive_response_fix_standard(rep_req)
        # endregion

        # region Check ExecutionReports
        exec_report3 = FixMessageExecutionReportOMS(self.data_set).set_default_replaced(self.ord_message)
        exec_report3.change_parameters({'Price': self.new_price, 'OrigClOrdID': cl_ord_id1})
        self.fix_verifier.check_fix_message_fix_standard(exec_report3,
                                                         key_parameters=['ClOrdID', 'OrdStatus', 'ExecType', 'Price'],
                                                         ignored_fields=['SettlDate', 'SettlType', 'Account'])
        # endregion
