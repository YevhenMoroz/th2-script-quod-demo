import logging
import select
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
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7358(TestCase):

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
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name("currency_3")
        self.fix_message.change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur})
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.approve = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.conf_block = ConfirmationOMS(self.data_set)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        self.rest_commission_sender.set_modify_fees_message(fee=self.data_set.get_fee_by_name('fee_vat'),
                                                            recalculate=True,
                                                            fee_type=self.data_set.get_misc_fee_type_by_name(
                                                                'value_added_tax'), comm_profile=commission_profile)
        self.rest_commission_sender.change_message_params({"venueID": self.data_set.get_venue_by_name("venue_2"),
                                                           "contraFirmCounterpartID": self.data_set.get_counterpart_id(
                                                               "contra_firm")})
        self.rest_commission_sender.send_post_request()
        rate = 5
        fee_amt = int(float(self.price) * float(self.qty) * rate / 10000)
        # endregion
        # region create order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        # endregion
        # region check order is create
        new_ignor_list = ['Currency', 'SecondaryOrderID', 'LastMkt', 'Text', 'SettlType']
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=new_ignor_list)
        # endregion
        # region check order is filled
        fill_ignor_list = ['ReplyReceivedTime', 'SettlCurrency', 'Currency', 'LastMkt', 'Text', 'SettlType',
                           'CommissionData']
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameter("MiscFeesGrp", '#')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=fill_ignor_list)
        # endregion
        # region book order
        new_avg_px = float(self.price) / 100
        self.all_instr.set_default_book(order_id)
        self.all_instr.update_fields_in_component('AllocationInstructionBlock',
                                                  {"InstrID": self.data_set.get_instrument_id_by_name("instrument_3"),
                                                   "AccountGroupID": self.client,
                                                   "Currency": self.data_set.get_currency_by_name("currency_3"),
                                                   'AvgPx': new_avg_px})
        responses = self.java_api_manager.send_message_and_receive_response(self.all_instr)
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        alloc_id = alloc_report[JavaApiFields.AllocInstructionID.value]
        # endregion
        # region check alloc instr
        all_ignore_fields = ['Account', 'AvgPx', 'tag5120', 'RootSettlCurrAmt', 'OrderAvgPx']
        alloc_instr_report = FixMessageAllocationInstructionReportOMS()
        alloc_instr_report.set_default_ready_to_book(self.fix_message)
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_instr_report, ignored_fields=all_ignore_fields)
        # endregion
        # region approve
        self.approve.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve)
        all_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value,
             JavaApiFields.AllocReportType.value: AllocationReportConst.AllocReportType_ACC.value},
            all_report.get_parameter('AllocationReportBlock'),
            'Check approving')
        # endregion
        # region allocate block
        self.conf_block.set_default_allocation(alloc_id)
        self.conf_block.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc,
                                                                         "InstrID": self.data_set.get_instrument_id_by_name(
                                                                             "instrument_3"),
                                                                         'Currency': self.currency_post_trade,
                                                                         "AvgPx": str(new_avg_px)})
        self.java_api_manager.send_message_and_receive_response(self.conf_block)
        # endregion
        # region check allocation block
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
             'MiscFeesList': {'MiscFeesBlock': [{"MiscFeeAmt": str(float(fee_amt)),
                                                 "MiscFeeBasis": "P",
                                                 "MiscFeeCurr": "GBP",
                                                 "MiscFeeRate": str(float(rate)),
                                                 "MiscFeeType": "VAT"}]}},
            conf_report.get_parameter('ConfirmationReportBlock'),
            'Check allocation')
        # endregion
        # region check confirmation report
        conf_ignore_fields = ["CommissionData", 'Account', "AvgPx", "Currency", "tag5120", 'OrderAvgPx']
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(
            self.fix_message)
        conf_report.change_parameters(
            {"NoMiscFees": {"NoMiscFees": [
                {'MiscFeeAmt': str(int(fee_amt)), 'MiscFeeCurr': self.data_set.get_currency_by_name("currency_2"),
                 'MiscFeeType': '22'}]}})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report, ignored_fields=conf_ignore_fields)
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

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
