import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7242(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_reqeust = DFDManagementBatchOMS(self.data_set)
        self.book_request = AllocationInstructionOMS(self.data_set)
        self.com_cur = self.data_set.get_currency_by_name('currency_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(self.environment.get_list_fe_environment()[0].user_1,
                                                 self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion
        # region Step 2
        self.trade_entry.set_default_trade(ord_id)
        self.java_api_manager.send_message(self.trade_entry)
        # endregion
        # region Step 3
        self.complete_reqeust.set_default_complete(ord_id)
        self.java_api_manager.send_message(self.complete_reqeust)
        self.book_request.set_default_book(ord_id)
        fee = "0.0005"
        self.book_request.update_fields_in_component("AllocationInstructionBlock",
                                                     {'RootMiscFeesList': {
                                                         'RootMiscFeesBlock': [{
                                                                                   'RootMiscFeeType': AllocationInstructionConst.RootMiscFeeType_EXC.value,
                                                                                   'RootMiscFeeAmt': fee,
                                                                                   'RootMiscFeeCurr': self.com_cur,
                                                                                   'RootMiscFeeBasis': "Absolute",
                                                                                   'RootMiscFeeRate': fee}]}})
        self.java_api_manager.send_message_and_receive_response(self.book_request)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]['RootMiscFeesList']['RootMiscFeesBlock'][0]
        self.java_api_manager.compare_values({'RootMiscFeeRate': "5.0E-4"}, allocation_report, "Check fee")
