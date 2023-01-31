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
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ConfirmationReportConst, \
    AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.java_api_wrappers.ors_messages.BookingCancelRequest import BookingCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7174(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.client2 = self.data_set.get_client('client_pt_2')  # MOClient2
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.unallocate = BlockUnallocateRequest()
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation = ConfirmationOMS(self.data_set)
        self.cancel_booking = BookingCancelRequest()
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        order_id = None
        qty = '100'
        price = '10'
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(price),
                                                                                            int(qty), 0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': qty},
                                                'Account': self.data_set.get_client_by_name('client_pt_1'),
                                                'Instrument': self.data_set.get_fix_instrument_by_name('instrument_1'),
                                                'Price': price,
                                                'ExDestination': exec_destination})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Order ID
            order_id = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region book order and verify values after it at order book (step 1)
        instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            'InstrID': instr_id})
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            self.result.get_parameter('OrdUpdateBlock'),
            'Check order sts')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value},
            self.result.get_parameter('AllocationReportBlock'),
            'Check block sts')
        booking_alloc_instr_id = self.result.get_parameter('AllocationReportBlock')['BookingAllocInstructionID']
        alloc_instr_id = self.result.get_parameter('AllocationReportBlock')['AllocInstructionID']
        # endregion

        # region approve block
        self.approve.set_default_approve(alloc_id=alloc_instr_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve)
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value},
            self.result.get_parameter('AllocationReportBlock'),
            'Check sts after approve')
        # endregion

        # region allocate block
        self.confirmation.set_default_allocation(alloc_id=alloc_instr_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {'InstrID': instr_id})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation)
        self.__return_result(responses, ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmTransType.value: ConfirmationReportConst.ConfirmTransType_NEW.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value},
            self.result.get_parameter('ConfirmationReportBlock'),
            'Check sts after allocation')
        # endregion

        # region Unallocate block
        self.unallocate.set_default(alloc_instr_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.unallocate)
        self.__return_result(responses, ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmTransType.value: ConfirmationReportConst.ConfirmTransType_CAN.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_CXL.value},
            self.result.get_parameter('ConfirmationReportBlock'),
            'Check sts after unallocation')
        # endregion

        # region unbook block
        self.cancel_booking.set_default(booking_alloc_instr_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.cancel_booking)
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
            self.result.get_parameter('OrdUpdateBlock'),
            'Check order sts')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_CXL.value},
            self.result.get_parameter('AllocationReportBlock'),
            'Check unbook sts')
        # endregion

        # region re-Book order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {'AccountGroupID': self.client2,
                                                                'InstrID': instr_id})
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            self.result.get_parameter('OrdUpdateBlock'), 'Check order booking sts after rebooking')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.AccountGroupID.value: self.client2},
            self.result.get_parameter('AllocationReportBlock'), 'Check order Account value after rebooking')
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
