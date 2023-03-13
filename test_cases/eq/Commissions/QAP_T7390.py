import logging
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7390(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.drop_copy = self.fix_env.drop_copy
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.qty = "4232"
        self.price = "4232"
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.account = self.data_set.get_account_by_name("client_counterpart_1_acc_1")
        self.no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(
            "instrument_3").change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': self.no_allocs, "Currency": self.cur, "ExDestination": self.mic})
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.drop_copy, self.test_id)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.confirmation = FixMessageConfirmationReportOMS(self.data_set)
        self.trade = TradeEntryOMS(self.data_set)
        self.dfd_conf = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fee
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(recalculate=True, fee=self.fee,
                                                            comm_profile=self.comm_profile).change_message_params(
            {"venueID": self.data_set.get_venue_by_name("venue_2")}).send_post_request()
        # endregion

        # region send order
        self.__send_fix_orders()
        # endregion

        # region execute order
        self.trade.set_default_trade(self.order_id, self.price, self.qty)
        self.trade.update_fields_in_component('TradeEntryRequestBlock', {'LastMkt': self.mic})
        self.java_api_manager.send_message(self.trade)
        # endregion

        # region complete order
        self.dfd_conf.set_default_complete(self.order_id)
        self.java_api_manager.send_message(self.dfd_conf)
        # endregion
        time.sleep(8)

        # region check calculated message
        exec_ignored_fields = ['Account', 'SettlCurrency', 'LastExecutionPolicy', 'Currency', 'SecondaryOrderID',
                               'LastMkt', 'VenueType', 'SecondaryExecID', 'GatingRuleCondName', 'GatingRuleName']
        self.exec_report.set_default_filled(self.new_order_single)
        self.exec_report.change_parameters({"MiscFeesGrp":"#"})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=exec_ignored_fields)
        # endregion

        # region check ready to book message
        alloc_ignored_fields = ['Account', 'tag5120', 'AvgPx', 'Currency', 'OrderAvgPx']
        self.alloc_report.set_default_ready_to_book(self.new_order_single)
        self.alloc_report.change_parameters({"NoRootMiscFeesList": "#"})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.alloc_report, ignored_fields=alloc_ignored_fields)
        # endregion

        # region check confirmation message
        no_misc_fees = {'NoMiscFees': [{"MiscFeeAmt": '8954.91', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}]}
        conf_ignored_fields = ['CommissionData', 'tag5120', 'AvgPx', 'Currency', 'OrderAvgPx', 'tag11245']
        self.confirmation.set_default_confirmation_new(self.new_order_single)
        self.confirmation.change_parameters({'NoMiscFees':no_misc_fees})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.confirmation, ignored_fields=conf_ignored_fields)
        # endregion

    def __send_fix_orders(self):
        self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        self.order_id = self.response[0].get_parameter("OrderID")

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
