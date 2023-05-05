import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7164(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.order_action_request = OrderActionRequest()
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur})
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("abs_amt")
        self.fee_type = self.data_set.get_misc_fee_type_by_name('stamp')
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.dfd_manage_batch = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        tree.getroot().find("automaticCalculatedReportEnabled").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(60)
        # endregion

        # region send fee and clcommission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        commission_profile_stamp = self.data_set.get_comm_profile_by_name('perc_amt')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile_stamp,
                                                            fee_type=self.fee_type)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_client_commission_message(client=self.client,
                                                                         comm_profile=self.comm_profile)
        self.rest_commission_sender.change_message_params({'venueID': self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region care send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_order_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region Set DiscloseExec = Manual
        self.order_action_request.set_default([order_id])
        self.java_api_manager.send_message_and_receive_response(self.order_action_request)
        order_notification = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, order_id). \
            get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.DiscloseExec.value: OrderReplyConst.DiscloseExec_M.value},
            order_notification, f'Verifying that DiscloseExec = M for order')
        # endregion

        # region split child order
        nos_rule = None
        trade_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.client_for_rule,
                self.mic,
                int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.submit_request.set_default_child_dma(order_id)
            self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
                'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"), 'AccountGroupID': self.client})
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        ord_notif_dma = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrdNotificationBlock.value)
        ord_id_dma = ord_notif_dma[JavaApiFields.OrdID.value]

        comm_list = {
            JavaApiFields.CommissionBasis.value: 'BPS',
            JavaApiFields.CommissionAmount.value: '0.002',
            JavaApiFields.CommissionRate.value: '1.0',
            JavaApiFields.CommissionAmountType.value: 'BRK',
            JavaApiFields.CommissionCurrency.value: self.com_cur
        }

        misc_list = {
            JavaApiFields.MiscFeeBasis.value: 'BPS',
            JavaApiFields.MiscFeeAmt.value: '0.002',
            JavaApiFields.MiscFeeRate.value: '1.0',
            JavaApiFields.MiscFeeType.value: 'BRK',
            JavaApiFields.MiscFeeCurr.value: self.com_cur
        }

        # check fee and commission of parent order
        exec_report_parent = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                    order_id).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        parent_exec_id = exec_report_parent[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ClientCommissionList.value:
                 {JavaApiFields.ClientCommissionBlock.value: [comm_list], JavaApiFields.MiscFeesList.value:
                     {JavaApiFields.MiscFeesBlock.value: [misc_list]}}},
            exec_report_parent,
            "Check fee and clcommission in the parent order")
        # endregion

        # check fee and commission of parent order
        exec_report_child = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                    [ord_id_dma,
                                                                     ExecutionReportConst.ExecType_TRD.value]).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ClientCommissionList.value:
                 {JavaApiFields.ClientCommissionBlock.value: [comm_list], JavaApiFields.MiscFeesList.value:
                     {JavaApiFields.MiscFeesBlock.value: [misc_list]}}},
            exec_report_child,
            "Check fee and clcommission in the child order")
        # endregion

        # region Exec Summary
        self.trade_entry_request.set_default_execution_summary(order_id, [parent_exec_id], self.price, self.qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region complete
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report,
            'Check order after complete')
        # endregion

        # region ComputeBooking
        new_avg_px = float(self.price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, parent_exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        root_misc = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[JavaApiFields.RootMiscFeesList.value][
            JavaApiFields.RootMiscFeesBlock.value][0]
        cl_comm = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[JavaApiFields.ClientCommissionList.value][
            JavaApiFields.ClientCommissionBlock.value][0]

        misc_list = {
            JavaApiFields.RootMiscFeeBasis.value: 'BPS',
            JavaApiFields.RootMiscFeeAmt.value: '0.002',
            JavaApiFields.RootMiscFeeRate.value: '1.0',
            JavaApiFields.RootMiscFeeType.value: 'BRK',
            JavaApiFields.RootMiscFeeCurr.value: self.com_cur
        }

        self.java_api_manager.compare_values(misc_list,
                                             root_misc,
                                             "Check Fee in the Booking Ticket")
        self.java_api_manager.compare_values(comm_list,
                                             cl_comm,
                                             "Check Fee in the Booking Ticket")
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
                                                                JavaApiFields.RootMiscFeesList.value:
                                                                    {JavaApiFields.RootMiscFeesBlock.value: [
                                                                        root_misc]},
                                                                "Qty": self.qty, "SettlCurrAmt": "2001"})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)

        # region step 3 - Check commission
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        alloc_report_fee = alloc_report[JavaApiFields.RootMiscFeesList.value][
            JavaApiFields.RootMiscFeesBlock.value][0]
        self.java_api_manager.compare_values(misc_list,
                                             alloc_report_fee,
                                             "Check Fee after booking")
        alloc_id = alloc_report["AllocInstructionID"]
        # endregion

        # region step 4 - Allocate order
        self.force_alloc.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.force_alloc)
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_3"), "AllocQty": self.qty,
                                                                      "AvgPx": new_avg_px})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(misc_list,
                                             confirm_report[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             "Check Fee after allocation")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(60)
        os.remove("temp.xml")
