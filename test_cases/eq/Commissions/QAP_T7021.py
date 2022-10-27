import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiManageSecurityBlock import RestApiManageSecurityBlock
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7021(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.cur = self.data_set.get_currency_by_name('currency_1')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.qty_to_display = '50'
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rest_api_manager = RestApiManager(session_alias=self.wa_connectivity, case_id=self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fee1 = self.data_set.get_fee_by_name('fee1')
        self.fee2 = self.data_set.get_fee_by_name('fee2')
        self.fee3 = self.data_set.get_fee_by_name('fee3')
        self.fee_type1 = self.data_set.get_misc_fee_type_by_name('stamp')
        self.fee_type2 = self.data_set.get_misc_fee_type_by_name('levy')
        self.fee_type3 = self.data_set.get_misc_fee_type_by_name('per_transac')
        self.params = {"Account": self.client,
                       'DisplayInstruction': {'DisplayQty': self.qty_to_display},
                       'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.client_acc,
                                                     'AllocQty': self.qty}]}}
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.manage_security_block = RestApiManageSecurityBlock(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        # self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee1, fee_type=self.fee_type1)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee2, fee_type=self.fee_type2)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee3, fee_type=self.fee_type3)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.manage_security_block.set_fee_exemption(False, False, True)
        self.rest_api_manager.send_post_request(self.manage_security_block)
        time.sleep(3)
        # endregion
        # region step 1-2
        self.submit_request.set_default_dma_limit()
        self.submit_request.update_fields_in_component("NewOrderSingleBlock", {
            "InstrID": self.data_set.get_instrument_id_by_name("instrument_3"), 'AccountGroupID': self.client,
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]}})

        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty),
                                                                         int(self.qty), 1)
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["OrdID"]
        cl_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["ClOrdID"]
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        post_trd_sts = exec_reply["PostTradeStatus"]
        exec_id = exec_reply["ExecID"]
        # endregion
        # region step 3
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, self.price, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            "ComputeBookingFeesCommissionsReplyBlock"]
        expected_levy = {'ExpectedFee': 'LEV'}
        expected_stamp = {'ExpectedFee': 'STA'}
        expected_per_trans = {'ExpectedFee': 'TRA'}
        self.java_api_manager.compare_values(expected_levy,
                                             {"ExpectedFee": str(
                                                 compute_reply["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Levy", VerificationMethod.CONTAINS)

        self.java_api_manager.compare_values(expected_stamp,
                                             {"ExpectedFee": str(
                                                 compute_reply["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Stamp", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 compute_reply["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Per Transac", VerificationMethod.NOT_CONTAINS)
        # endregion
        # region step 4
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"RootMiscFeesList": compute_reply["RootMiscFeesList"],
                                                     "AccountGroupID": self.client,
                                                     "InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(expected_levy,
                                             {"ExpectedFee": str(
                                                 alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Levy", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_stamp,
                                             {"ExpectedFee": str(
                                                 alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Stamp", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Per Transac", VerificationMethod.NOT_CONTAINS)
        alloc_id = alloc_report["AllocInstructionID"]
        # endregion
        # region step 5
        self.force_alloc.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.force_alloc)
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(expected_levy,
                                             {"ExpectedFee": str(
                                                 confirm_report["MiscFeesList"]["MiscFeesBlock"])},
                                             "Check Levy", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_stamp,
                                             {"ExpectedFee": str(
                                                 confirm_report["MiscFeesList"]["MiscFeesBlock"])},
                                             "Check Stamp", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 confirm_report["MiscFeesList"]["MiscFeesBlock"])},
                                             "Check Per Transac", VerificationMethod.NOT_CONTAINS)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.manage_security_block.set_fee_exemption(False, False, False)
        self.rest_api_manager.send_post_request(self.manage_security_block)
