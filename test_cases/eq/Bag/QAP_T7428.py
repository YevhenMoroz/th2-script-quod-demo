import logging
import os
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7428(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(account="client_pt_1")
        self.nos2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(account="client_pt_1")
        self.price = self.nos.get_parameter("Price")
        self.qty = self.nos.get_parameter("OrderQtyData")["OrderQty"]
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.book_request = AllocationInstructionOMS(self.data_set)
        self.approve_request = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.alloc_request = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        resp = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)
        ord_id = resp[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        # endregion
        # region Step 1-3
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        orders_id = [ord_id, ord_id2]
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        # endregion
        # region Step 4
        qty_of_bag = str(int(int(self.qty) * 2))
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, int(self.price),
                                                                                          int(self.qty), 0)
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_TER.value}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Check wave")
        # endregion
        # region Step 5
        self.complete_request.set_default_complete_for_some_orders(orders_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        # endregion
        # region Step 6-8
        self.book_request.set_default_book(ord_id)
        self.book_request.update_fields_in_component("AllocationInstructionBlock",
                                                     {"InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.book_request)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value},
            allocation_report, 'Check booking')
        # endregion
        # region Step 9
        self.approve_request.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_request)
        expected_result = {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                           JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check approve')
        # endregion
        # region Step 10-12
        self.alloc_request.set_default_allocation(alloc_id)
        self.alloc_request.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.account,
                                                                            "InstrID": self.data_set.get_instrument_id_by_name(
                                                                                "instrument_2")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_request)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        actually_result = {
            JavaApiFields.ConfirmStatus.value: confirm_report[JavaApiFields.ConfirmStatus.value],
            JavaApiFields.MatchStatus.value: confirm_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                             f'Check statuses of confirmation of {self.account}')
        # endregion
        # region Step 13
        self.complete_request.set_default_uncomplete(ord_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_request)
        dfd_reply = \
            self.java_api_manager.get_last_message(ORSMessageType.DFDManagementBatchReply.value).get_parameters()[
                "DFDManagementBatchReplyBlock"]
        self.java_api_manager.compare_values({"FreeNotes": f"{alloc_id} cannot be cancelled"}, dfd_reply,
                                             'Check that uncomplete was not processed', VerificationMethod.CONTAINS)
        # endregion
