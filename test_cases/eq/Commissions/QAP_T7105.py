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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import AllocationInstructionConst, ExecutionReportConst, \
    OrderReplyConst, JavaApiFields, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7105(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send fees and commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        comm_rate = '5'
        misc_fee_amt = str(int(int(self.price) * int(self.qty) / 10000 * int(comm_rate)))
        # endregion
        # region check order ExecutionReports
        no_misc = {"MiscFeeAmt": misc_fee_amt, "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}
        comm_data = {"Commission": misc_fee_amt, "CommType": "3"}
        ignored_fields = ['GatingRuleName', 'GatingRuleCondName']
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report.change_parameters(
            {'ReplyReceivedTime': "*", 'Currency': self.cur, 'LastMkt': "*", 'Text': "*",
             "Account": self.client, "MiscFeesGrp": {"NoMiscFees": [no_misc]}, "CommissionData": comm_data})
        execution_report.remove_parameters(['SettlCurrency'])
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=ignored_fields)
        # endregion

        # region book order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock', {
            'ClientCommissionList': {'ClientCommissionBlock': [
                {'CommissionAmountType': AllocationInstructionConst.CommissionAmountType_BRK.value,
                 'CommissionAmount': misc_fee_amt,
                 'CommissionBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_PERCENTAGE.value,
                 'CommissionCurrency': self.com_cur,
                 'CommissionRate': comm_rate}]},
            'RootMiscFeesList': {'RootMiscFeesBlock': [{'RootMiscFeeType': "EXC",
                                                        'RootMiscFeeAmt': misc_fee_amt,
                                                        'RootMiscFeeCurr': self.com_cur,
                                                        'RootMiscFeeBasis': AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
                                                        'RootMiscFeeRate': comm_rate}]},
            "AccountGroupID": self.client,
            "InstrID": self.data_set.get_instrument_id_by_name(
                "instrument_3")
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Message on booking", responses)
        ord_update_message = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.PostTradeStatus.value: ord_update_message[JavaApiFields.PostTradeStatus.value],
                           JavaApiFields.DoneForDay.value: ord_update_message[JavaApiFields.DoneForDay.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value],
                           JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value]}

        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
             JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            actually_result,
            'Compare actually and expected results  from step 3')
        # endregion
        # region check 35 = J message
        list_of_ignored_fields = ['RootCommTypeClCommBasis', 'Account', 'OrderAvgPx']
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(
            self.fix_message)
        no_root_misc = {"RootMiscFeeBasis": "2", "RootMiscFeeCurr": self.com_cur,
                        "RootMiscFeeType": no_misc['MiscFeeType'],
                        "RootMiscFeeRate": '5', "RootMiscFeeAmt": no_misc['MiscFeeAmt']}
        alloc_report.change_parameters(
            {"Account": self.client, "AvgPx": "*", "Currency": "*", "tag5120": "*",
             'RootOrClientCommission': comm_data['Commission'], 'RootCommTypeClCommBasis': comm_data['CommType'],
             "RootOrClientCommissionCurrency": self.com_cur,
             'NoRootMiscFeesList': {"NoRootMiscFeesList": [no_root_misc]}, "RootSettlCurrAmt": "*"})
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ignored_fields=list_of_ignored_fields)
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {"Account": self.client,
                 "ExDestination": self.mic,
                 "Currency": self.data_set.get_currency_by_name("currency_3")})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
