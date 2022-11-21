import logging
import time
from pathlib import Path
from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7391(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "4231"
        self.price = "4231"
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)

    def run_pre_conditions_and_steps(self):
        new_avg_px = str(int(self.price) / 100)
        commission_rate = str(float(1))
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.__step_precondition()
        tuple_orders_indicators: tuple = self.__step_first(instrument_id)
        exec_id = self.__step_second(tuple_orders_indicators[0])
        tuple_for_allocation = self.__step_third(tuple_orders_indicators[1], tuple_orders_indicators[0], exec_id, new_avg_px,
                                     commission_rate, commission_rate, instrument_id)
        self.__step_fourth(tuple_for_allocation[0], new_avg_px, instrument_id, tuple_for_allocation[1])

    def __step_precondition(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(recalculate=True).send_post_request()
        time.sleep(10)

    def __step_first(self, instrument_id):
        self.order_submit.set_default_dma_limit()
        self.order_submit.remove_fields_from_component('NewOrderSingleBlock',['SettlCurrency'])
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Creating DMA order", responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        return order_id, cl_ord_id

    def __step_second(self, order_id):
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": self.qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Fully Filled)', responses)
        actually_result = dict()
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        actually_result.update(
            {JavaApiFields.TransExecStatus.value: execution_report[JavaApiFields.TransExecStatus.value]})
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, actually_result,
            f'Check {JavaApiFields.TransExecStatus.value} from step 2')
        self.java_api_manager.key_is_absent(JavaApiFields.ClientCommissionList.value, execution_report,
                                            "Check that Client Commission is absent step 2")
        exec_id = execution_report[JavaApiFields.ExecID.value]
        return exec_id

    def __step_third(self, cl_ord_id, order_id, exec_id, new_avg_px, commission_amount, commission_rate, instrument_id):
        tuple_for_allocation_instruction = self.__send_compute_misc_fee_request(cl_ord_id, order_id, exec_id,
                                                                                new_avg_px, commission_amount,
                                                                                commission_rate)
        return self.__send_allocation_instruction_request(order_id, tuple_for_allocation_instruction[0], new_avg_px,
                                                          tuple_for_allocation_instruction[1], exec_id, instrument_id)

    def __send_compute_misc_fee_request(self, cl_ord_id, order_id, exec_id, new_avg_px, commission_amount,
                                        commission_rate):
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty, new_avg_px,
                                                                                        self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('ComputeBookingFeesCommissionsRequest', responses)
        expected_commission = {
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_ABS.value,
            JavaApiFields.CommissionAmount.value: commission_amount,
            JavaApiFields.CommissionRate.value: commission_rate,
            JavaApiFields.CommissionCurrency.value: self.currency_post_trade
        }
        commission_for_allocation_instruction = \
            self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value][
                JavaApiFields.ClientCommissionList.value]
        commission_actual = commission_for_allocation_instruction[JavaApiFields.ClientCommissionBlock.value][0]

        self.java_api_manager.compare_values(expected_commission, commission_actual,
                                             f'Check that Client Commission presents in {ORSMessageType.ComputeBookingFeesCommissionsReply.value}')
        return commission_for_allocation_instruction, expected_commission

    def __send_allocation_instruction_request(self, order_id, client_commisison, new_avg_px,
                                              client_commission_expected, exec_id, instrument_id):
        self.allocation_instruction.set_default_book(order_id)
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': new_avg_px,
                                                                   'Qty': self.qty,
                                                                   "InstrID": instrument_id,
                                                                   'Currency': self.currency_post_trade,
                                                                   JavaApiFields.ClientCommissionList.value: client_commisison,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                           'ExecID': exec_id,
                                                                                           'ExecPrice': new_avg_px}]}
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Allocation Instruction", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        commission_actually = \
            allocation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(client_commission_expected, commission_actually,
                                             'Check Client Commission in Allocation Instruction')
        return alloc_id, client_commission_expected

    def __step_fourth(self, alloc_id, new_avg_px, instrument_id, commission_expected):
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.account,
            'AllocQty': self.qty,
            'AvgPx': new_avg_px,
            "InstrID": instrument_id
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message('Confirmation', responses)
        confirmation_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[JavaApiFields.ConfirmationReportBlock.value]
        actual_commission = confirmation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(commission_expected, actual_commission, 'Check commission from step 4')

    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()