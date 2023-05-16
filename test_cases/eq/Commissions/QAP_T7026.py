import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsVenues, OMSFee
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7026(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send commission and fees
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_fees_message(comm_profile=self.perc_amt, fee=OMSFee.fee1)
        self.commission_sender.change_message_params({"venueID": OmsVenues.venue_2.value})
        self.commission_sender.send_post_request()
        self.commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt)
        self.commission_sender.send_post_request()
        time.sleep(5)
        # endregion
        # region step 1
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component("NewOrderSingleBlock", {"SettlCurrency": "GBp",
                                                                               "InstrID": self.data_set.get_instrument_id_by_name(
                                                                                   "instrument_3"),
                                                                               'AccountGroupID': self.client,
                                                                               'ListingList': {'ListingBlock': [{
                                                                                                                    'ListingID': self.data_set.get_listing_id_by_name(
                                                                                                                        "listing_2")}]}})
        self.java_api_manager.send_message_and_receive_response(self.submit_request)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["OrdID"]
        cl_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["ClOrdID"]
        # endregion
        # region step 2
        self.trade_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        expected_result = {"TransExecStatus": "FIL", "ExecCommission": "1.0", "ClientCommission": "1.0"}
        self.java_api_manager.compare_values(expected_result, exec_reply,
                                             "Compare TransExecStatus, ExecCommission and ClientCommission")
        # endregion
        # region step 3
        self.complete_message.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        post_trd_sts = exec_reply["PostTradeStatus"]
        exec_id = exec_reply["ExecID"]
        # endregion
        # region step 4
        cross_price = (int(self.price) / 100) * 2
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, cross_price, self.client)
        self.compute_request.update_fields_in_component("ComputeBookingFeesCommissionsRequestBlock",
                                                        {"RecomputeInSettlCurrency": "Yes", "SettlCurrency": "UAH",
                                                         "SettlCurrFxRate": "2", "SettlCurrFxRateCalc": "Multiply"})

        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            "ComputeBookingFeesCommissionsReplyBlock"]
        expected_result_comm = {'CommissionCurrency': 'UAH', 'CommissionBasis': 'PCT', 'CommissionRate': '5.0',
                                'CommissionAmount': '2.0', 'CommissionAmountType': 'BRK'}
        expected_result_fee = {'RootMiscFeeBasis': 'P', 'RootMiscFeeType': 'EXC', 'RootMiscFeeCurr': 'UAH',
                               'RootMiscFeeRate': '5.0', 'RootMiscFeeAmt': '2.0'}
        self.java_api_manager.compare_values(expected_result_comm,
                                             compute_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
                                             "Compare ClientCommission")
        self.java_api_manager.compare_values(expected_result_fee,
                                             compute_reply["RootMiscFeesList"]["RootMiscFeesBlock"][0],
                                             "Compare RootMiscFees")
        # endregion
        # region step 5
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"ClientCommissionList": compute_reply["ClientCommissionList"],
                                                     "RootMiscFeesList": compute_reply["RootMiscFeesList"],
                                                     "AccountGroupID": self.client,
                                                     "InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                              JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(expected_result_comm,
                                             alloc_report["ClientCommissionList"]["ClientCommissionBlock"][0],
                                             "Compare ClientCommission")
        self.java_api_manager.compare_values(expected_result_fee,
                                             alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"][0],
                                             "Compare RootMiscFees")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
