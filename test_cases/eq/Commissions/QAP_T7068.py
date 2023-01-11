import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, ExecutionReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7068(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.currency = self.data_set.get_currency_by_name('currency_2')
        self.currency_GBp = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '100'
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = '20'
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client,
                                                                         comm_profile=self.comm_profile).change_message_params(
            {'venueListID': 1}).send_post_request()
        # endregion
        # region create DMA  order
        self.submit_request.set_default_dma_limit()
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["OrdID"]
        cl_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["ClOrdID"]
        # endregion

        # region execute DMA order
        commission_amount = '1'
        expected_commission_amount_dict = {JavaApiFields.CommissionAmount.value: str(float(commission_amount))}
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
                                                             "Currency": self.currency_GBp,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": self.qty,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.mic,
                                                             "OrdQty": self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = exec_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(expected_commission_amount_dict,
                                             exec_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Checking that order has properly Commission (step 2)')
        self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value:
                                                  ExecutionReportConst.TransExecStatus_FIL.value},
                                             exec_report,
                                             f'Checking that order has properly {JavaApiFields.TransExecStatus.value} (step 3)')
        # endregion

        # region step 3: Book CO order

        # part 1: send compute_misc_fee_request
        new_avg_px = float(self.price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        # end of part

        # part 2: Book CO order
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        gross_amt = float(new_avg_px) * float(self.qty)

        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {JavaApiFields.ClientCommissionList.value: compute_reply[
                                                        JavaApiFields.ClientCommissionList.value],
                                                     "AccountGroupID": self.client,
                                                     "AvgPx": new_avg_px,
                                                     'GrossTradeAmt': gross_amt,
                                                     "InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        alloc_id = alloc_report[JavaApiFields.ClAllocID.value]
        # end_of_part

        # part step 3: Check expected result

        self.java_api_manager.compare_values(expected_commission_amount_dict,
                                             alloc_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             f'Checking that {JavaApiFields.CommissionAmount.value} has properly value (step 3)')
        # end_of_part
        # endregion

        # region step 4: Check that confirmation has properly ClientCommissionAmount

        # part 1:Approve block
        self.force_alloc.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.force_alloc)
        # end_of_part

        # part 2: Allocate block
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc,
                                                                      'AvgPx': new_avg_px,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        # end_of_part

        # part 3: Check ConfirmationReport
        self.java_api_manager.compare_values(expected_commission_amount_dict,
                                             confirm_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             f'Checking that {JavaApiFields.CommissionAmount.value} has properly value (step 4)')
        self.java_api_manager.compare_values(
            {JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.AffirmStatus_AFF.value}, confirm_report,
            f'Checking that {JavaApiFields.ConfirmStatus.value} has properly status')
        # end_of_part

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
