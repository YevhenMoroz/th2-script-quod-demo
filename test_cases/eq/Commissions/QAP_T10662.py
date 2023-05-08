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
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T10662(TestCase):
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
        self.comm_cur = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.qty = '10000'
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur,
             'OrderQtyData': {'OrderQty': self.qty}})
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.profile_bas_amt = self.data_set.get_comm_profile_by_name('bas_amt')
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set configuration on backend (precondition)
        tree = ET.parse(self.local_path)
        tree.getroot().find("ignoreRecomputeInConfirmation").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS CS")
        time.sleep(60)
        # endregion

        # region send fee
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(recalculate=True,
                                                            comm_profile=self.profile_bas_amt).change_message_params(
            {"venueID": self.data_set.get_venue_by_name("venue_2")})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region care send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_order_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region manual execute order
        expected_result_comm = {
            JavaApiFields.RootMiscFeeBasis.value: 'B',
            JavaApiFields.RootMiscFeeAmt.value: '1.0',
            JavaApiFields.RootMiscFeeRate.value: '5.0',
            JavaApiFields.RootMiscFeeType.value: 'EXC',
            JavaApiFields.RootMiscFeeCurr.value: self.comm_cur
        }
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        self.trade_entry_request.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.mic})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                             ExecutionReportConst.ExecType_TRD.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        exec_id = exec_report[JavaApiFields.ExecID.value]
        # self.java_api_manager.compare_values({JavaApiFields.RootMiscFeesList.value:
        #                                           {JavaApiFields.RootMiscFeesBlock.value: [expected_result_comm]}},
        #                                      exec_report, 'Check Fee in the execution')
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        # endregion

        # region ComputeBooking
        new_avg_px = float(self.price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        root_misc = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[JavaApiFields.RootMiscFeesList.value][
            JavaApiFields.RootMiscFeesBlock.value][0]

        self.java_api_manager.compare_values(expected_result_comm,
                                             root_misc,
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
        self.java_api_manager.compare_values(expected_result_comm,
                                             alloc_report_fee,
                                             "Check Fee after booking")
        alloc_id = alloc_report["AllocInstructionID"]
        # endregion

        # region step 4 - Allocate order
        expected_result_fee = {
            JavaApiFields.MiscFeeBasis.value: 'B',
            JavaApiFields.MiscFeeAmt.value: '0.01',
            JavaApiFields.MiscFeeRate.value: '5.0',
            JavaApiFields.MiscFeeType.value: 'EXC',
            JavaApiFields.MiscFeeCurr.value: self.comm_cur
        }
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
        self.java_api_manager.compare_values(expected_result_fee,
                                             confirm_report[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             "Check Fee after allocation")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS CS")
        time.sleep(60)
        os.remove("temp.xml")
