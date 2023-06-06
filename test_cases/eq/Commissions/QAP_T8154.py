import logging
import time

from custom import basic_custom_actions as bca, basic_custom_actions
from pathlib import Path

from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields,  ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiVenueListMessages import RestApiVenueListMessages
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8154(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rest_commission_sender = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_list_request = RestApiVenueListMessages(self.data_set)
        self.venue = self.data_set.get_venue_id('paris')
        self.rest_wash_book_message = RestApiWashBookRuleMessages(self.data_set)
        self.client = self.data_set.get_client_by_name('client_com_1')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.venue_id = self.data_set.get_venue_list('test_auto')
        self.order_submit = OrderSubmitOMS(data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up venue list
        venue_list = [self.venue]
        self.venue_list_request.modify_venue_list(venue_list)
        self.rest_api_manager.send_post_request(self.venue_list_request)
        # region sent clcommission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.comm_profile).change_message_params(
            {'venueListID': self.venue_id}).send_post_request()
        # endregion

        # region create order (step 1)
        qty = '100'
        price = '10'
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.OrdID.value]
        cl_ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.ClOrdID.value]
        # endregion

        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'EUR',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '5.0',
                                JavaApiFields.CommissionAmount.value: '50.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK',
                                JavaApiFields.CommissionAmountSubType.value: 'OTH'}

        # region manual execute order (step 1)
        self.trade_request.set_default_trade(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = exec_reply[JavaApiFields.ExecID.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                           JavaApiFields.ClientCommissionList.value: {
                               JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}}
        self.java_api_manager.compare_values(expected_result, exec_reply,
                                             "Check commissions after Execution")
        # endregion

        # region complete order (step 1)
        self.complete_message.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        post_trd_sts = exec_reply["PostTradeStatus"]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             exec_reply, "Check order is completed")
        # endregion

        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'EUR',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '5.0',
                                JavaApiFields.CommissionAmount.value: '1.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK'}

        # region get commission from Booking Ticket (step 2)
        cross_price = (int(price) / 100) * 2
        self.compute_request.set_list_of_order_alloc_block(cl_ord_id, ord_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(qty, exec_id, price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(qty, cross_price, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)

        self.java_api_manager.compare_values(
            {JavaApiFields.ClientCommissionList.value: {
                JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}},
            compute_reply,
            "Check commission in the booking ticket")
        # endregion

        # region book order (step 2)
        self.alloc_instr.set_default_book(ord_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"ClientCommissionList": compute_reply[
                                                        JavaApiFields.ClientCommissionList.value],
                                                     "AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ClientCommissionList.value: {
                JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}},
            alloc_report,
            "Check commissions after booking")
        # endregion

        # delete venue from the VenueList (step 3)
        self.venue_list_request.set_default_venue_list()
        self.rest_api_manager.send_post_request(self.venue_list_request)
        # endregion
        time.sleep(5)

        # region create order (step 4)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        qty = self.order_submit.get_parameter('NewOrderSingleBlock')['OrdQty']
        price = self.order_submit.get_parameter('NewOrderSingleBlock')['Price']
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                             "ClOrdID": basic_custom_actions.client_orderid(
                                                                                 9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.OrdID.value]
        cl_ord_id = ord_notif.get_parameter(JavaApiFields.OrdNotificationBlock.value)[JavaApiFields.ClOrdID.value]
        # endregion

        # region manual execute order (step 4)
        self.trade_request.set_default_trade(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()
        exec_id = exec_reply[JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}
        self.java_api_manager.compare_values(expected_result, exec_reply[
            JavaApiFields.ExecutionReportBlock.value],
                                             "Check order is filled")
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecutionReportBlock.value: JavaApiFields.ClientCommissionList.value}, exec_reply,
            "Check commission is not present after Execution", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region complete order (step 4)
        self.complete_message.set_default_complete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        post_trd_sts = exec_reply["PostTradeStatus"]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             exec_reply, "Check order is completed")
        # endregion

        # region get commission from Booking Ticket (step 5)
        compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        cross_price = (int(price) / 100) * 2
        compute_request.set_list_of_order_alloc_block(cl_ord_id, ord_id, post_trd_sts)
        compute_request.set_list_of_exec_alloc_block(qty, exec_id, price, post_trd_sts)
        compute_request.set_default_compute_booking_request(qty, price, self.client)
        self.java_api_manager.send_message_and_receive_response(compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()

        self.java_api_manager.compare_values(
            {JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value: JavaApiFields.ClientCommissionList.value},
            compute_reply,
            "Check comission isn't in the booking ticket", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region book order (step 5)
        alloc_instr = AllocationInstructionOMS(self.data_set)
        alloc_instr.set_default_book(ord_id)
        alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocationReportBlock.value: JavaApiFields.ClientCommissionList.value},
            alloc_report,
            "Check comissions is absent after booking", VerificationMethod.NOT_CONTAINS)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.venue_list_request.set_default_venue_list()
        self.rest_api_manager.send_post_request(self.venue_list_request)

