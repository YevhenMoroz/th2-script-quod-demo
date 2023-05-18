import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
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


class QAP_T8657(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.client_acc = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.comm_cur = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.submit_request = OrderSubmitOMS(self.data_set).set_default_dma_limit()
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty = '300'
        self.price = '2'
        self.listing_id = self.data_set.get_listing_id_by_name("listing_2")
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.comm_type_broker = self.data_set.get_commission_amount_type('broker')
        self.comm_type_retail = self.data_set.get_commission_amount_type('retail')
        self.comm_type_sales = self.data_set.get_commission_amount_type('sales')
        self.commission2 = self.data_set.get_commission_by_name("commission2")
        self.commission3 = self.data_set.get_commission_by_name("commission3")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fee
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt,
                                                                         client=self.client).change_message_params(
            {'commissionAmountType': self.comm_type_broker, 'venueID': self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt,
                                                                         client=self.client).change_message_params(
            {'commissionAmountType': self.comm_type_retail, 'clCommissionID': self.commission2.value,
             'clCommissionName': self.commission2.name, 'venueID': self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt,
                                                                         client=self.client).change_message_params(
            {'commissionAmountType': self.comm_type_sales, 'clCommissionID': self.commission3.value,
             'clCommissionName': self.commission3.name, 'venueID': self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region send dma order
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                               'ListingList': {'ListingBlock': [{
                                                                                   'ListingID': self.listing_id}]},
                                                                               'InstrID': self.instr_id,
                                                                               'OrdQty': self.qty, "Price": self.price})
        trade_rule = None
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, float(self.price),
                                                                                            int(self.qty), 2)

            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            exec_report = self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
            order_id = exec_report[JavaApiFields.OrdID.value]
            cl_order_id = exec_report[JavaApiFields.ClOrdID.value]
            exec_id = exec_report[JavaApiFields.ExecID.value]
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check clcommissions after execution
        self.__check_comm_amount_type(exec_report, 'Execution')
        # endregion

        # region ComputeBooking
        new_avg_px = float(self.price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_booking_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)
        cl_comm = compute_booking_reply[JavaApiFields.ClientCommissionList.value][
            JavaApiFields.ClientCommissionBlock.value]
        self.__check_comm_amount_type(compute_booking_reply, 'Compute Booking Fees Commission Request')
        # endregion

        # region step 3 - Book order
        gross_amt = float(new_avg_px) * float(self.qty)
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock",
                                                               {"AccountGroupID": self.client,
                                                                "AvgPx": new_avg_px,
                                                                'GrossTradeAmt': gross_amt,
                                                                "InstrID": self.data_set.get_instrument_id_by_name(
                                                                    "instrument_3"), 'Currency': self.cur,
                                                                JavaApiFields.ClientCommissionList.value:
                                                                    {
                                                                        JavaApiFields.ClientCommissionBlock.value: cl_comm},
                                                                "Qty": self.qty})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)

        # region step 3 - Check commission
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.__check_comm_amount_type(alloc_report, 'Book')
        alloc_id = alloc_report["AllocInstructionID"]
        # endregion

        # region step 4 - Allocate order
        self.force_alloc.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.force_alloc)
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_3"), "AllocQty": self.qty,
                                                                      "AvgPx": new_avg_px})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_first_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.__check_comm_amount_type(confirm_report, 'Allocation')
        # endregion

    def __check_comm_amount_type(self, report, action):
        com_type_list_exp = sorted([self.comm_type_broker, self.comm_type_retail, self.comm_type_sales])
        # extract actual data
        com_type_list_act = []
        for i in range(3):
            commission = report[JavaApiFields.ClientCommissionList.value][
                JavaApiFields.ClientCommissionBlock.value][i][JavaApiFields.CommissionAmountType.value]
            com_type_list_act.append(commission)
        com_type_list_act = sorted(com_type_list_act)
        # create dictionary with data from list
        exp_dict = {}
        y = 1
        for i in com_type_list_exp:
            exp_dict[y] = i
            y += 1
        act_dict = {}
        y = 1
        for i in com_type_list_act:
            act_dict[y] = i
            y += 1
        # compare 2 dicts
        self.java_api_manager.compare_values(exp_dict, act_dict, f'Check commissions are present after {action}')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
