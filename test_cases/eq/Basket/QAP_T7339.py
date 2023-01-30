import os
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.oms.FixMessageListCancelRequestOMS import FixMessageListCancelRequestOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7339(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.ord_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.message)
        list_id = response[0].get_parameters()['ListID']
        cl_ord_id1 = response[0].get_parameters()['OrdListStatGrp']['NoOrders'][0]['ClOrdID']
        cl_ord_id2 = response[0].get_parameters()['OrdListStatGrp']['NoOrders'][1]['ClOrdID']
        # endregion

        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message, 1)
        # endregion

        # region Check ExecutionReports
        list_to_ignore = ['CxlQty', 'SettlDate', 'ExpireDate', 'Account', 'GatingRuleCondName', 'GatingRuleName']
        self.fix_verifier.check_fix_message_fix_standard(exec_report1, list_to_ignore)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2, list_to_ignore)
        # endregion

        # region Send OrderCancelReplaceRequest on order
        self.ord_message.change_parameter('ClOrdID', cl_ord_id1)
        rep_req = FixMessageOrderCancelRequestOMS().set_default(self.ord_message)
        self.fix_manager.send_message_fix_standard(rep_req)
        # endregion

        # region Check basket ExecutionReport
        exec_report4 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled(self.ord_message)
        self.fix_verifier.check_fix_message_fix_standard(exec_report4,
                                                         ignored_fields=list_to_ignore)
        # endregion

        # region Send OrderCancelReplaceRequest on basket
        rep_req = FixMessageListCancelRequestOMS().set_default_ord_list(list_id)
        self.fix_manager.send_message_fix_standard(rep_req)
        # endregion

        # region Check list status
        list_status = FixMessageListStatusOMS().set_default_list_status(self.message)
        list_status.change_parameters({'ListOrderStatus': '4', 'ListID': list_id})
        self.fix_verifier.check_fix_message_fix_standard(list_status, key_parameters=['ListOrderStatus'])
        # endregion

        # region Check orders ExecutionReports
        exec_report5 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled_list(self.message)
        self.fix_verifier.check_fix_message_fix_standard(exec_report5, ignored_fields=list_to_ignore)
        exec_report5 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled_list(self.message, 1)
        self.fix_verifier.check_fix_message_fix_standard(exec_report5,
                                                         ignored_fields=['CxlQty', 'SettlDate', 'ExpireDate', 'Account',
                                                                         'OrigClOrdID'])
        # endregion
