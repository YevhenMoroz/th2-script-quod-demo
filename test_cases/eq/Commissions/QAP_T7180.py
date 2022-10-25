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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import AllocationInstructionConst, OrderReplyConst, \
    JavaApiFields, ConfirmationReportConst, AllocationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7180(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.qty = '7180'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')  # MOClient_EUREX
        self.venue = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.client = self.data_set.get_client('client_com_1')  # CLIENT_COMM_1
        self.client_acc = self.data_set.get_account_by_name('client_com_1_acc_1')  # CLIENT_COMM_1_SA1
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.comp_comm = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.dfd_manage = DFDManagementBatchOMS(self.data_set)
        self.confirmation = ConfirmationOMS(self.data_set)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        order_id = new_order_single = cl_order_id = None
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name('commission_with_minimal_value'))
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA order (precondition)
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names,
                self.venue,
                float(self.price))
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
            cl_order_id = response[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
        # endregion

        # region  execute DMA order (precondition)
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        self.__return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_id = self.result.get_parameter(JavaApiFields.ExecutionReportBlock.value)['ExecID']
        # endregion

        # region  complete DMA order (precondition)
        self.dfd_manage.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.dfd_manage)
        self.__return_result(responses, ORSMessageType.ExecutionReport.value)
        # endregion

        # region step 1
        # region get values from booking ticket
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.set_default_book(order_id)
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.comp_comm.set_list_of_order_alloc_block(cl_order_id, order_id, post_trade_sts)
        self.comp_comm.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trade_sts)
        self.comp_comm.set_default_compute_booking_request(self.qty)
        self.comp_comm.update_fields_in_component(JavaApiFields.ComputeBookingFeesCommissionsRequestBlock.value,
                                                  {'AccountGroupID': self.client, 'AvgPx': '0.100000000'})
        responses = self.java_api_manager.send_message_and_receive_response(self.comp_comm)
        self.__return_result(responses, ORSMessageType.ComputeBookingFeesCommissionsReply.value)
        comm_list = {'ClientCommissionBlock': [
            {'CommissionAmount': '100.0', 'CommissionRate': '100.0', 'CommissionBasis': 'ABS',
             'CommissionCurrency': 'GBP', 'CommissionAmountType': 'BRK'}]}
        # region book order
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.currency,
                                                                   "AccountGroupID": self.client,
                                                                   'ClientCommissionList': comm_list
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion

        # region check actual result from step 1
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            self.result.get_parameter(JavaApiFields.OrdUpdateBlock.value),
            'Check order Post Trade sts')
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmationService.value: AllocationInstructionConst.ConfirmationService_MAN.value},
            self.result.get_parameter(JavaApiFields.AllocationReportBlock.value),
            'Check block ConfirmationService')
        alloc_instr_id = self.result.get_parameter(JavaApiFields.AllocationReportBlock.value)[
            JavaApiFields.ClientAllocID.value]
        # endregion

        # region step 2
        self.approve_message.set_default_approve(alloc_instr_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_message)
        # endregion

        # region check actual result from step 2
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value},
            self.result.get_parameter(JavaApiFields.AllocationReportBlock.value),
            'Check block Match Sts and Block Status ')
        # endregion

        # region step 5
        self.confirmation.set_default_allocation(alloc_instr_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc,
                                                                           "InstrID": instrument_id,
                                                                           "AllocQty": self.qty})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation)
        # endregion

        # check result after step 5
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             'ClientCommissionList': comm_list},
            self.result.get_parameter(JavaApiFields.AllocationReportBlock.value),
            'Check block sts in the Allocation')
        self.__return_result(responses, ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.AffirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             'ClientCommissionList': comm_list},
            self.result.get_parameter(JavaApiFields.ConfirmationReportBlock.value),
            'Check block sts in the Confirmation')
        conf_id = self.result.get_parameter(JavaApiFields.ConfirmationReportBlock.value)['ConfirmationID']
        # endregion

        # region step 6
        self.confirmation.set_default_amend_allocation(conf_id, alloc_instr_id, '15', self.qty)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc,
                                                                           "InstrID": instrument_id})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation)
        self.__return_result(responses, ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.AffirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value, "AvgPx": "15.0",
             'ClientCommissionList': comm_list},
            self.result.get_parameter(JavaApiFields.ConfirmationReportBlock.value),
            'Check block sts in the Amended Confirmation')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
