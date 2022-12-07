import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7247(TestCase):

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
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.fee = self.data_set.get_fee_by_name("fee1")
        self.fee_type = self.data_set.get_misc_fee_type_by_name("other")
        self.intr_type = self.data_set.get_instr_type('equity')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee,
                                                            comm_profile=self.comm_profile,
                                                            fee_type=self.fee_type).change_message_params(
            {'venueID': self.venue, "instrType": self.intr_type,
             "orderCommissionProfileID": self.comm_profile}).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        # endregion
        # region Check ExecutionReports
        self.exec_report.set_default_filled(self.fix_message)
        no_misc = {'NoMiscFees': [{'MiscFeeAmt': '1', 'MiscFeeCurr': self.com_cur, 'MiscFeeType': '7'}]}
        self.exec_report.change_parameters(
            {'Currency': self.cur, 'SecondaryOrderID': '*', "NoMiscFees": no_misc, 'Text': '*', 'LastMkt': self.mic,
             "CommissionData": "*", "ExecBroker": "*", "tag5120": "*", "NoParty": "*", "QuodTradeQualifier": "*",
             'BookID': "*", "OrderID": self.order_id})
        self.exec_report.remove_parameters(['TradeReportingIndicator', 'Parties', 'SettlCurrency'])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report)
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
                 "Currency": self.cur})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            self.order_id = self.response[0].get_parameter("OrderID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
