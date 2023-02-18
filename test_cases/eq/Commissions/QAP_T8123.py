import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T8123(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.response = None
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '8123'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        new_order_single = trade_rule = order_id = None
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_commissions()
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA  and fill it step 1
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names,
                self.venue,
                float(self.price)
            )
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0
                                                                                            )
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)

        # region check 35=8 message step 2
        expected_result = {'ExecType': 'F'}
        last_excution_trade = self.__get_fix_message(expected_result)
        self.java_api_manager.compare_values(expected_result, last_excution_trade,
                                             'Check that ExecSts = F (part of step 2)', VerificationMethod.CONTAINS)
        last_execution_calculated = self.__get_fix_message({'ExecType': 'B'})
        print(last_execution_calculated)
        list_of_ignored_fields = ['SettlType', 'GatingRuleName', 'GatingRuleCondName']
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.set_default_calculated(self.fix_message)
        amount = str(round(float(self.qty) * float(self.price) / 10000 * 5.0, 3))
        expected_agent_fees = {'MiscFeeAmt': amount, 'MiscFeeCurr': self.currency_post_trade, 'MiscFeeType': '12'}
        self.java_api_manager.compare_values(expected_agent_fees, last_execution_calculated['NoMiscFees']['NoMiscFees'][0],
                                             'Check that Calculated execution has Agent Fees (part of step 2)', VerificationMethod.CONTAINS)
        execution_report.remove_parameter('Parties')
        execution_report.add_tag({'SecondaryOrderID': '*'})
        execution_report.remove_parameter('TradeReportingIndicator')
        execution_report.change_parameters({'QuodTradeQualifier': '*', 'BookID': '*',
                                            'Currency': self.currency, 'NoParty': '*', 'CommissionData': '*',
                                            'tag5120': '*', 'ExecBroker': '*',
                                            'NoMiscFees': [expected_agent_fees]})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()

    def __get_fix_message(self, parameter: dict):
        for i in range(len(self.response)):
            for j in parameter.keys():
                if self.response[i].get_parameters()[j] == parameter[j]:
                    return self.response[i].get_parameters()
