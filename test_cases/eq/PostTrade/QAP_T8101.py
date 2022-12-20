import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8101(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "10"
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.alloc_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create order
        self.nos.update_fields_in_component("NewOrderReplyBlock",
                                            {"VenueAccount": {"VenueActGrpName": self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep["OrdID"]
        cl_ord_id = self.nos.get_parameter("NewOrderReplyBlock")["ClOrdID"]
        expected_result = {JavaApiFields.TransStatus.value: "OPN", JavaApiFields.UnsolicitedOrder.value: "Y"}
        actually_result = {JavaApiFields.TransStatus.value: ord_rep[JavaApiFields.TransStatus.value],
                           JavaApiFields.UnsolicitedOrder.value: ord_rep[JavaApiFields.UnsolicitedOrder.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check order status')
        # endregion
        # region execute and complete order
        self.exec_rep.set_default_trade(cl_ord_id)
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, {"OrdID": order_id})
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        expected_result = {JavaApiFields.TransExecStatus.value: "FIL"}
        actually_result = {JavaApiFields.TransExecStatus.value: exec_report[JavaApiFields.TransExecStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check execution status')
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_request)
        # endregion

        # region book order
        self.all_instr.set_default_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"AccountGroupID": self.client,
                                                   "InstrID": self.data_set.get_instrument_id_by_name("instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value}
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}

        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking')
        # endregion

        # region approve block
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
        # endregion
        # region allocate block

        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.alloc_account,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             f'Check statuses of confirmation of {self.alloc_account}')

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
