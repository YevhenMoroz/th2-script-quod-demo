import logging
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from custom import basic_custom_actions as bca
from test_framework.java_api_wrappers.java_api_constants import (
    JavaApiFields, ExecutionReportConst, AllocationInstructionConst, OrderReplyConst, AllocationReportConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7191(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt_gbp")
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.currency = self.data_set.get_currency_by_name('currency_2')
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client, comm_profile=self.perc_amt)
        self.rest_commission_sender.send_post_request()
        # endregion

        # region step 1-2: Create and execute DMA order
        new_order_single = trade_rule = None
        self.submit_request.set_default_dma_limit()
        listing_id = self.data_set.get_listing_id_by_name('listing_2')
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.ListingList.value: {
                JavaApiFields.ListingBlock.value: [{JavaApiFields.ListingID.value: listing_id}]},
            JavaApiFields.InstrID.value: instrument_id,
            JavaApiFields.AccountGroupID.value: self.client
        })
        qty = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        price = self.submit_request.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        commission_rate = '5.0'
        commission_amount = str(float(qty) * float(price) / 10000 * float(commission_rate))
        expected_result_client_commission = {JavaApiFields.CommissionAmount.value: commission_amount,
                                             JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
                                             JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEE_BASIS_PCT.value,
                                             JavaApiFields.CommissionRate.value: commission_rate,
                                             JavaApiFields.CommissionCurrency.value: self.currency}
        list_of_orders = []
        list_of_executions = []
        list_of_cl_ord_id = []
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client, self.mic, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client, self.mic,
                                                                                            float(price), int(qty), 0)
            for counter in range(2):
                self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                    JavaApiFields.ClOrdID.value: bca.client_orderid(9)
                })
                self.java_api_manager.send_message_and_receive_response(self.submit_request, response_time=15_000)
                order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                     f"'{JavaApiFields.TransStatus.value}': '{OrderReplyConst.TransStatus_OPN.value}'").get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
                list_of_orders.append(order_reply[JavaApiFields.OrdID.value])
                list_of_cl_ord_id.append(order_reply[JavaApiFields.ClOrdID.value])
                self.java_api_manager.compare_values(
                    {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                    order_reply, f'Verify that order created (step 1) for {list_of_orders[counter]}')
                execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                          ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
                list_of_executions.append(execution_report[JavaApiFields.ExecID.value])
                self.java_api_manager.compare_values(expected_result_client_commission,
                                                     execution_report[JavaApiFields.ClientCommissionList.value][
                                                         JavaApiFields.ClientCommissionBlock.value][0],
                                                     f'Verify that Client commission was calculated (step 2) for {list_of_executions[counter]}')
        except Exception as e:
            logger.error(f'Something go wrong {e}')
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
        # enderegion

        # region step 4 Send ComputeMiscFeeRequest for orders:
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        for counter in range(2):
            self.compute_request.clear_lists()
            self.compute_request.set_list_of_order_alloc_block(list_of_cl_ord_id[counter], list_of_orders[counter],
                                                               post_trd_sts)
            self.compute_request.set_list_of_exec_alloc_block(qty, list_of_executions[counter], price, post_trd_sts)
            self.compute_request.set_default_compute_booking_request(qty, str(float(price)/100), self.client)
            self.java_api_manager.send_message_and_receive_response(self.compute_request)
            compute_reply = self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
                    get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
            client_commission_actually = compute_reply[JavaApiFields.ClientCommissionList.value]
            self.java_api_manager.compare_values(expected_result_client_commission,
                                                 client_commission_actually[JavaApiFields.ClientCommissionBlock.value][
                                                     0],
                                                 f'Verify that client commission presents for ComputeBookingFeesCommissionsReply for {list_of_orders[counter]} (part of step 4)')

            self.allocation_instruction_message.set_default_book(list_of_orders[counter])
            gross_currency_amt = str(float(qty) * float(price)/100)
            self.allocation_instruction_message.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                                           {
                                                                               JavaApiFields.GrossTradeAmt.value: gross_currency_amt,
                                                                               JavaApiFields.AvgPx.value: price,
                                                                               JavaApiFields.Qty.value: qty,
                                                                               JavaApiFields.AccountGroupID.value: self.client,
                                                                               JavaApiFields.Currency.value: self.currency,
                                                                               JavaApiFields.InstrID.value: instrument_id,
                                                                               JavaApiFields.ClientCommissionList.value: client_commission_actually,
                                                                               JavaApiFields.ExecAllocList.value: {
                                                                                   JavaApiFields.ExecAllocBlock.value: [
                                                                                       {JavaApiFields.ExecQty.value: qty,
                                                                                        JavaApiFields.ExecID.value: list_of_executions[counter],
                                                                                        JavaApiFields.ExecPrice.value: price}]},
                                                                           })
            self.java_api_manager.send_message_and_receive_response(self.allocation_instruction_message)
            allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[JavaApiFields.AllocationReportBlock.value]
            expected_client_commission_list = allocation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
            self.java_api_manager.compare_values({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                                                  JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_UNM.value},
                                                 allocation_report, 'Verify that block created (part of step 4)')
            self.java_api_manager.compare_values(expected_result_client_commission, expected_client_commission_list, f'Verify that Client Commission properly calcualted for block (order is {list_of_orders[counter]}) (part of step 4)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
