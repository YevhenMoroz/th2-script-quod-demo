import logging
import os
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
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
class QAP_T7534(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "2998"
        self.price = "2998"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.send_default_fee()
        self.__send_fix_order()
        self.__verify_commissions()

    @try_except(test_id=Path(__file__).name[:-3])
    def __send_fix_order(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.data_set.get_venue_client_names_by_name("client_com_1_venue_2"),
                self.data_set.get_mic_by_name("mic_2"), float(self.price), float(self.price), int(self.qty),
                int(self.qty), 1)

            self.new_order_single.set_default_dma_limit(
                "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2")
                    , "Currency": self.data_set.get_currency_by_name("currency_3")})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        except Exception as E:
            logger.error(f'Your exception is {E}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        self.rest_commission_sender.clear_fees()

    @try_except(test_id=Path(__file__).name[:-3])
    def __verify_commissions(self):
        value_of_commission = '0.01'
        list_of_ignored_fields = ['ReplyReceivedTime', 'Account',
                                  'SettlCurrency', 'Currency', 'LastMkt', 'SettlType', 'Text']
        self.fix_execution_report.change_parameters({'CommissionData': {'Commission': value_of_commission,
                                                                        'CommType': '3'},
                                                     'MiscFeesGrp': {
                                                         'NoMiscFees': [{'MiscFeeAmt': value_of_commission,
                                                                         'MiscFeeCurr': self.data_set.get_currency_by_name(
                                                                             'currency_2'),
                                                                         'MiscFeeType': '4'}]}})
        self.fix_execution_report.set_default_filled(self.new_order_single)
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_report,
                                                         ignored_fields=list_of_ignored_fields)
