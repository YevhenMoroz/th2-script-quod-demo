import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.BlockChangeConfirmationServiceRequest import \
    BlockChangeConfirmationServiceRequest
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7490(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_manager = FixManager(self.ss_connectivity)
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client('client_pt_8')  # MOClient7 Fully manual with one account
        self.account1 = self.data_set.get_account_by_name("client_pt_6_acc_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')  # MOClient7_PARIS
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.change_confirm = BlockChangeConfirmationServiceRequest()
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.booking_cancel = BookingCancelRequest()
        self.unallocate = BlockUnallocateRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region Split Booking
        order_id = response[0].get_parameters()['OrderID']
        self.all_instr.set_split_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name(
                                                      "instrument_2"),
                                                      "AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report1 = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id1 = allocation_report1[JavaApiFields.ClAllocID.value]
        booking_id = allocation_report1[JavaApiFields.ClientAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report1[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report1[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking')

        allocation_report2 = \
            self.java_api_manager.get_first_message(ORSMessageType.AllocationReport.value, "APP").get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id2 = allocation_report2[JavaApiFields.ClAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report2[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report2[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking 2')
        # endregion
        # region approve blocks
        self.approve.set_default_approve(alloc_id1)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')

        self.approve.set_default_approve(alloc_id2)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve2')
        # endregion
        # region allocate block
        self.confirm.set_default_allocation(alloc_id1)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.account1,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2"), "AllocQty": "50"})
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
                                             f'Check statuses of confirmation of {self.account1}')

        self.confirm.set_default_allocation(alloc_id2)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.account1,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_2"), "AllocQty": "50"})
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
                                             f'Check statuses of confirmation 2 of {self.account1}')
        # endregion
        # region unbook
        self.booking_cancel.set_default(booking_id)
        self.java_api_manager.send_message_and_receive_response(self.booking_cancel)
        cancel_reply = self.java_api_manager.get_last_message(ORSMessageType.BookingCancelReply.value).get_parameters()[
            "MessageReply"]["MessageReplyBlock"]
        self.java_api_manager.compare_values({"ErrorCD": "QUOD-24806"}, cancel_reply[0], 'Check unsuccessful unbook')
        self.java_api_manager.compare_values({"ErrorCD": "QUOD-24806"}, cancel_reply[1], 'Check unsuccessful unbook 2')
        # endregion
        # region unallocate
        self.unallocate.set_default(alloc_id1)
        self.java_api_manager.send_message(self.unallocate)
        self.unallocate.set_default(alloc_id2)
        self.java_api_manager.send_message(self.unallocate)
        # endregion
        # region unbook
        self.booking_cancel.set_default(booking_id)
        self.java_api_manager.send_message_and_receive_response(self.booking_cancel)
        cancel_reply = self.java_api_manager.get_last_message(ORSMessageType.BookingCancelReply.value).get_parameters()[
            "BookingCancelReplyBlock"]
        self.java_api_manager.compare_values({"AllocInstructionID": booking_id, "AllocStatus": "CXL"}, cancel_reply,
                                             'Check successful unbook')
        # endregion
