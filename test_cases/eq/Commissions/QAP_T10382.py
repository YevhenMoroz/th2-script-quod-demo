import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10382(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.qty = '100'
        self.price = '10'
        self.order_submit = OrderSubmitOMS(data_set)
        self.venue1 = self.data_set.get_venue_by_name('venue_1')
        self.venue2 = self.data_set.get_venue_by_name('venue_4')
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        self.listing1 = self.data_set.get_listing_id_by_name("listing_6")
        self.listing2 = self.data_set.get_listing_id_by_name("listing_7")
        self.listing3 = self.data_set.get_listing_id_by_name("listing_8")
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_7")
        self.comm2 = self.data_set.get_commission_by_name("commission2")
        self.chix_mic = self.data_set.get_mic_by_name('mic_4')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("clientCommissions/eventType").text = 'DFD'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(40)

        # region Send commission and fees
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt)
        self.commission_sender.change_message_params({"venueID": self.venue1})
        self.commission_sender.send_post_request()
        self.commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt)
        self.commission_sender.change_message_params(
            {"venueID": self.venue2, 'clCommissionID': self.comm2.value, 'clCommissionName': self.comm2.name})
        self.commission_sender.send_post_request()
        # endregion

        # region create order (step 1)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
                'ListingList': {'ListingBlock': [{'ListingID': self.listing1}, {'ListingID': self.listing2},
                                                 {'ListingID': self.listing3}]}
            },
        )
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.OrdID.value]
        cl_ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.ClOrdID.value]
        # endregion

        # region first manual order execution (precondition)
        qty_to_exec = str(int(self.qty)/2)
        self.trade_request.set_default_trade(ord_id, self.price, qty_to_exec)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecutionReportBlock.value: JavaApiFields.ClientCommissionList.value}, exec_report,
            "Check commission is not present in the Execution (LastMkt = XPAR)", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region manual execute order (precondition)
        self.trade_request.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.chix_mic})
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecutionReportBlock.value: JavaApiFields.ClientCommissionList.value}, exec_report,
            "Check commission is not present in the Execution (LastMkt = CHIX)", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region complete order (precondition)
        self.complete_message.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        post_trd_sts = exec_reply["PostTradeStatus"]
        exec_id = exec_reply["ExecID"]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             exec_reply, "Check order is completed")
        # endregion

        # region get commission and fee from Booking Ticket(precondition)
        cross_price = (int(self.price) / 100) * 2
        self.compute_request.set_list_of_order_alloc_block(cl_ord_id, ord_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, cross_price, self.client)
        self.compute_request.update_fields_in_component("ComputeBookingFeesCommissionsRequestBlock",
                                                        {"RecomputeInSettlCurrency": "Yes",
                                                         "SettlCurrFxRate": "2", "SettlCurrFxRateCalc": "Multiply"})

        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value: JavaApiFields.ClientCommissionList.value},
            compute_reply,
            "Check booking ticket doesn't contain commission", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region book order (precondition)
        self.alloc_instr.set_default_book(ord_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"AccountGroupID": self.client,
                                                     "InstrID": self.instr_id, "AvgPx": self.price,
                                                     "GrossTradeAmt": '2000'})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocationReportBlock.value: JavaApiFields.ClientCommissionList.value},
            alloc_report,
            "Check booking doesn't contain clcommission", VerificationMethod.NOT_CONTAINS)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.commission_sender.clear_commissions()
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
        time.sleep(40)
