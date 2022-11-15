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
from datetime import datetime
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationInstructionConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6999(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.price = '1.111'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        self.rest_commission_sender.clear_commissions()
        time.sleep(10)
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile)
        self.rest_commission_sender.send_post_request()
        time.sleep(10)
        # endregion

        # region create DMA  orders (precondition)
        list_of_client_order_ids = []
        list_of_order_ids = []
        for i in range(3):
            self.order_submit.set_default_dma_limit()
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
                'InstrID': instrument_id,
                'AccountGroupID': self.client,
                'OrdQty': self.qty,
                'Price': self.price,
                "ClOrdID": bca.client_orderid(9) + Path(__file__).name[:-3]
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            print_message('Create DMA  order', responses)
            list_of_order_ids.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
            list_of_client_order_ids.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value])
            # endregion

        # region Trade DMA orders (step 1)
        list_of_exec_ids = []
        commission_rate = str(float(5))
        commission_amount = str(float(commission_rate) * float(self.qty) * float(self.price) / 10000)
        expected_client_commission = {
            JavaApiFields.CommissionAmountType.value: AllocationInstructionConst.CommissionAmountType_BRK.value,
            JavaApiFields.CommissionBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_PERCENTAGE.value,
            JavaApiFields.CommissionAmount.value: commission_amount,
            JavaApiFields.CommissionRate.value: commission_rate,
            JavaApiFields.CommissionCurrency.value: self.currency_post_trade}
        for order_id in list_of_order_ids:
            self.execution_report.set_default_trade(order_id)
            self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                             {
                                                                 "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                     "instrument_2"),
                                                                 "Side": "Buy",
                                                                 "LastTradedQty": self.qty,
                                                                 "VenueExecID": bca.client_orderid(9),
                                                                 "LastVenueOrdID": (
                                                                         tm(datetime.utcnow().isoformat()) + bd(
                                                                     n=2)).date().strftime(
                                                                     '%Y-%m-%dT%H:%M:%S'),
                                                                 "LastPx": self.price,
                                                                 "OrdType": "Limit",
                                                                 "Price": self.price,
                                                                 "Currency": self.currency,
                                                                 "ExecType": "Trade",
                                                                 "TimeInForce": "Day",
                                                                 "LeavesQty": self.qty,
                                                                 "CumQty": self.qty,
                                                                 "AvgPrice": self.price,
                                                                 "LastMkt": self.venue_mic,
                                                                 "OrdQty": self.qty
                                                             })
            responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
            print_message(f'Trade DMA  order {order_id}', responses)
            actually_result = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                       ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value]
            list_of_exec_ids.append(actually_result[JavaApiFields.ExecID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, actually_result,
                'Compare actually and expected result from step 1 (concerning ExecSts)')
            commission_actually: dict = \
                actually_result[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
            commission_actually.update({JavaApiFields.CommissionAmount.value: str(
                round(float(commission_actually[JavaApiFields.CommissionAmount.value]), 5))})
            self.java_api_manager.compare_values(expected_client_commission, commission_actually,
                                                 'Check that client commission correctly calculated (step 1)')

        # endregion

        # region step 2 and 3
        new_avg_px = str(float(self.price) / 100)
        common_list = []
        common_list.extend(list_of_client_order_ids)
        common_list.extend(list_of_order_ids)
        for index in range(3):
            self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(common_list[index],
                                                                                      common_list[index + 3],
                                                                                      OrderReplyConst.PostTradeStatus_RDY.value)
        for exec_id in list_of_exec_ids:
            self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                     OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(str(int(self.qty) * 3),
                                                                                        new_avg_px,
                                                                                        self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('ComputeBookingFeesCommissionsRequest', responses)
        compute_reply = self.java_api_manager.get_last_message(ORSMessageType.ComputeBookingFeesCommissionsReply.value). \
            get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        commission_amount_expected = str(float(commission_amount) * 3)[0:4]
        expected_client_commission.update({JavaApiFields.CommissionAmount.value: commission_amount_expected})
        client_commission_for_allocation_instruction = compute_reply[JavaApiFields.ClientCommissionList.value]
        self.java_api_manager.compare_values(expected_client_commission, client_commission_for_allocation_instruction[
            JavaApiFields.ClientCommissionBlock.value][0],
                                             "Check client commissiont in step 3")

        # endregion

        # region step 4
        gross_amt = float(new_avg_px) * float(self.qty)
        exec_alloc_list = []
        for exec_id in list_of_exec_ids:
            exec_alloc_list.append({'ExecQty': self.qty, 'ExecID': exec_id, 'ExecPrice': self.price})
        self.allocation_instruction.set_default_book(list_of_order_ids[0])
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"OrdAllocList": {"OrdAllocBlock": [{"OrdID": list_of_order_ids[0]},
                                                                                                   {"OrdID": list_of_order_ids[1]},
                                                                                                   {"OrdID": list_of_order_ids[2]}]}})
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_amt,
                                                                   'AvgPx': new_avg_px,
                                                                   'Qty': str(int(self.qty)*3),
                                                                   "InstrID": instrument_id,
                                                                   'Currency': self.currency_post_trade,
                                                                   JavaApiFields.ClientCommissionList.value: client_commission_for_allocation_instruction,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': exec_alloc_list}
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Book orders", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        commission_actually = \
            allocation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0]
        self.java_api_manager.compare_values(expected_client_commission, commission_actually,
                                             'Check Client Commission in Allocation Instruction (step 4)')
        expected_result_of_status = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value
        }
        self.java_api_manager.compare_values(expected_result_of_status, allocation_report,
                                             'Check AllocationReport statuses (step 4)')
        # endregion

    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
