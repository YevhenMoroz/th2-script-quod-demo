import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, OrderReplyConst, \
    ConfirmationReportConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T8956(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.bo_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = "10000"
        self.price = self.fix_message.get_parameter("Price")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name("currency_3")
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur})
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.conf_block = ConfirmationOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        commission_profile_for_fee = self.data_set.get_comm_profile_by_name('amt_plus_client')
        self.rest_commission_sender.set_modify_fees_message(comm_profile=commission_profile_for_fee)
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_2")})
        self.rest_commission_sender.send_post_request()
        commission_profile_for_clcomm = self.data_set.get_comm_profile_by_name('sixbps')
        self.rest_commission_sender.set_modify_client_commission_message(comm_profile=commission_profile_for_clcomm,
                                                                         client=self.client)
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        cl_order_id = self.response[0].get_parameter("ClOrdID")
        exec_id = self._get_fix_message({'ExecType': 'F'})[JavaApiFields.ExecID.value]
        # endregion

        # region check order is create
        new_ignor_list = ['Currency', 'SecondaryOrderID', 'LastMkt', 'Text', 'SettlType', 'GatingRuleCondName',
                          'GatingRuleName']
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=new_ignor_list)
        # endregion

        # region check order is filled
        fill_ignor_list = ['ReplyReceivedTime', 'SettlCurrency', 'Currency', 'LastMkt', 'Text', 'SettlType',
                           'CommissionData', 'GatingRuleCondName', 'GatingRuleName']
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {"MiscFeesGrp": {'NoMiscFees': [{'MiscFeeAmt': '10.006', 'MiscFeeCurr': 'GBP', 'MiscFeeType': '4'}]}})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=fill_ignor_list)
        # endregion

        # region book order
        avg_price = '0.2'
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, avg_price, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            "ComputeBookingFeesCommissionsReplyBlock"]
        expected_result_comm = {'CommissionCurrency': self.currency_post_trade, 'CommissionBasis': 'BPS',
                                'CommissionRate': '6.0',
                                'CommissionAmount': '1.2', 'CommissionAmountType': 'BRK'}
        expected_result_fee = {'RootMiscFeeBasis': 'P', 'RootMiscFeeType': 'EXC',
                               'RootMiscFeeCurr': self.currency_post_trade,
                               'RootMiscFeeRate': '0.5', 'RootMiscFeeAmt': '10.006'}
        self.java_api_manager.compare_values(expected_result_comm,
                                             compute_reply["ClientCommissionList"]["ClientCommissionBlock"][0],
                                             "Compare ClientCommission")
        self.java_api_manager.compare_values(expected_result_fee,
                                             compute_reply["RootMiscFeesList"]["RootMiscFeesBlock"][0],
                                             "Compare RootMiscFees")

        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"ClientCommissionList": compute_reply["ClientCommissionList"],
                                                     "RootMiscFeesList": compute_reply["RootMiscFeesList"],
                                                     "AccountGroupID": self.client,
                                                     "InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_3"), "Qty": self.qty, "AvgPx": self.price})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        # endregion

        # region check alloc instr
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                              JavaApiFields.BookingAllocInstructionID.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        alloc_id = alloc_report[JavaApiFields.AllocInstructionID.value]
        self.java_api_manager.compare_values(expected_result_comm,
                                             alloc_report["ClientCommissionList"]["ClientCommissionBlock"][0],
                                             "Compare ClientCommission")
        self.java_api_manager.compare_values(expected_result_fee,
                                             alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"][0],
                                             "Compare RootMiscFees")
        # endregion

        # # region approve
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        all_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocReportType.value: AllocationReportConst.AllocReportType_ACC.value},
            all_report,
            'Check approving')
        # endregion

        # region allocate block
        self.conf_block.set_default_allocation(alloc_id)
        self.conf_block.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc,
                                                                         "InstrID": self.data_set.get_instrument_id_by_name(
                                                                             "instrument_3"),
                                                                         'Currency': self.currency_post_trade,
                                                                         "AllocQty": self.qty, "AvgPx": self.price})
        self.java_api_manager.send_message_and_receive_response(self.conf_block)
        # endregion

        # region check allocation block
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameter(
            JavaApiFields.ConfirmationReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             'MiscFeesList': {'MiscFeesBlock': [{"MiscFeeAmt": '10.006',
                                                 "MiscFeeBasis": "P",
                                                 "MiscFeeCurr": self.currency_post_trade,
                                                 "MiscFeeRate": '0.5',
                                                 "MiscFeeType": "EXC"}]}},
            conf_report,
            'Check allocation')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_orders(self):
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()

    def _get_fix_message(self, parameter: dict):
        for i in range(len(self.response)):
            print(self.response[i].get_parameters())
            for j in parameter.keys():
                if self.response[i].get_parameters()[j] == parameter[j]:
                    return self.response[i].get_parameters()
