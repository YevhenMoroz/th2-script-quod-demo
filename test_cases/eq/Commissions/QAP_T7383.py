import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7383(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.change_params = {'Account': self.client, "Currency": self.cur, "ExDestination": self.mic}
        self.fix_message.change_parameters(self.change_params)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.comm = self.data_set.get_commission_by_name("commission1")
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.fix_alloc_report = FixMessageAllocationInstructionReportOMS()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commissions
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee,
                                                            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(commission=self.comm,
                                                                         comm_profile=self.comm_profile).send_post_request()
        # endregion

        # region send order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)

            responses = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = responses[0].get_parameter("OrderID")
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check exec
        no_misc = {"MiscFeeAmt": '1', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}
        comm_data = {"Commission": "1", "CommType": "3"}
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report.change_parameters(
            {'ReplyReceivedTime': "*", 'Currency': self.cur, 'LastMkt': "*", 'Text': "*",
             "Account": self.client, "MiscFeesGrp": {"NoMiscFees": [no_misc]}, "CommissionData": comm_data})
        execution_report.remove_parameters(
            ['SettlCurrency'])
        self.fix_verifier.check_fix_message_fix_standard(execution_report)
        # endregion

        # region book order
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        new_avg_px = str(float(self.price) / 100)
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': new_avg_px,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.cur,
                                                                   "AccountGroupID": self.client
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion

        # region check block values
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        self.java_api_manager.compare_values({'NetMoney': '20.0'},
                                             alloc_report,
                                             "Check NetMoney in the Alloc Report")
        # endregion

        # region check total fees
        ignored_fields = ['Account', 'AvgPx', 'tag5120', 'RootSettlCurrAmt']
        self.fix_alloc_report.set_default_ready_to_book(self.fix_message)
        self.fix_alloc_report.change_parameters(
            {'NoRootMiscFeesList': '#', 'ClientCommissionList': '#', 'RootCommTypeClCommBasis': '#'})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.fix_alloc_report, ignored_fields=ignored_fields)
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
