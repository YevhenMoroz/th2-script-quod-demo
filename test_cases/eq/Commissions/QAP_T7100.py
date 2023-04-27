import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7100(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "100"
        self.price = "10"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.perc_qty = self.data_set.get_comm_profile_by_name("perc_qty")
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.java_api_conn = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_conn, self.test_id)
        self.dfd_management_request = DFDManagementBatchOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.confirmation = ConfirmationOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(account=self.account,
                                                                         comm_profile=self.perc_qty
                                                                         ).send_post_request()
        # endregion

        # region Send order
        self.__send_fix_order()
        order_id = self.response[0].get_parameter("OrderID")
        # endregion

        # region manual execute order
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        message = 'Check values after manual execution'
        self.__verify_commissions(message)
        # endregion

        # region complete order
        self.dfd_management_request.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_management_request)
        message = 'Check values of order after complete'
        self.__verify_order_value(message)
        # endregion

        # region book order
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"AccountGroupID": self.client,
                                                     "InstrID": self.instr_id, "AvgPx": self.price,
                                                     "GrossTradeAmt": '2000'})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocationReportBlock.value: JavaApiFields.ClientCommissionList.value}, alloc_report,
            "Check commission isn't present in the block", VerificationMethod.NOT_CONTAINS)
        alloc_id = alloc_report[JavaApiFields.AllocationReportBlock.value][JavaApiFields.ClAllocID.value]
        # endregion

        # region allocate order
        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'EUR',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '10.0',
                                JavaApiFields.CommissionAmount.value: '10.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK'}
        self.confirmation.set_default_allocation(alloc_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.account,
                                                                           "InstrID": self.instr_id,
                                                                           "AvgPx": self.price})
        self.java_api_manager.send_message_and_receive_response(self.confirmation)
        confirmation = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameter(
            JavaApiFields.ConfirmationReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ClientCommissionList.value: {
            JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}}, confirmation,
            "Check commission after Allocation")
        # endregion

    def __send_fix_order(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(
            "instrument_3").change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2"),
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)

    def __verify_commissions(self, message):
        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'GBP',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '10.0',
                                JavaApiFields.CommissionAmount.value: '1.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK',
                                JavaApiFields.CommissionAmountSubType.value: 'OTH'}
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ClientCommissionList.value: {
            JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}}, actually_result,
            event_name=message)

    def __verify_order_value(self, message):
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, actually_result,
            message)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
