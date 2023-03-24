import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    SubmitRequestConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9013(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.dc_connectivity = self.fix_env.drop_copy
        self.trd_request = TradeEntryOMS(self.data_set)
        self.dfd_batch_request = DFDManagementBatchOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.ord_sub = OrderSubmitOMS(self.data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1,
            self.environment.get_list_fe_environment()[0].desk_ids[0], SubmitRequestConst.USER_ROLE_1.value)
        self.qty = self.ord_sub.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        child_qty = str(int(self.qty)//2)
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        ord_id_care = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]

        self.ord_sub.set_default_child_care(self.environment.get_list_fe_environment()[0].user_1,
                                                  self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  SubmitRequestConst.USER_ROLE_1.value, ord_id_care)
        self.ord_sub.update_fields_in_component("NewOrderSingleBlock",{"OrdQty": child_qty})
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        child_ord_id_care = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]

        self.ord_sub.set_default_child_dma(ord_id_care)
        self.java_api_manager.send_message_and_receive_response(self.ord_sub)
        child_ord_id_dma = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        # endregion
        # region step 1
        self.trd_request.set_default_trade(child_ord_id_care, exec_qty=child_qty)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value},
                                             exec_report_block, 'Check first execution')
        # endregion
        # region step 2
        self.trd_request.set_default_trade(child_ord_id_dma, exec_qty=child_qty)
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value},
                                             exec_report_block, 'Check second execution')
        # endregion
        # region step 3
        self.dfd_batch_request.set_default_complete(ord_id_care)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch_request)
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
                                             exec_report_block, 'Check dfd status execution after complete')
        # endregion
        # region step 4
        self.allocation_instruction.set_default_book(ord_id_care)
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value}
        self.java_api_manager.compare_values(expected_result, allocation_report, 'Check step 4')
        # endregion
        # region step 5
        self.ssh_client.send_command("~/quod/script/site_scripts/db_endOfDay_postgres")
        status = self.db_manager.execute_query(f"select ordstatus from ordr where ordid='{ord_id_care}';")[0][0]
        self.java_api_manager.compare_values({"Sts": "EXP"}, {"Sts": status}, "Check order status")
        # endregion

