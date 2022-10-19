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
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7549(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()
        self.buy_side = self.environment.get_list_fix_environment()[0].buy_side
        self.sell_side = self.environment.get_list_fix_environment()[0].sell_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.client_venue_paris = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination_paris = self.data_set.get_mic_by_name('mic_1')
        self.fix_manager = FixManager(self.sell_side, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        new_order_qty = 15000
        try:
            price = self.fix_message.get_parameter('Price')
            self.fix_message.update_fields_in_component('OrderQtyData', {'OrderQty': new_order_qty})
            nos_rule_paris = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.buy_side, self.client_venue_paris, self.exec_destination_paris, float(price))
            trade_rule_paris = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.buy_side, self.client_venue_paris, self.exec_destination_paris, float(price), int(new_order_qty),
                0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.execution_report.set_default_filled(self.fix_message)
            list_of_ignored_fields = ['ReplyReceivedTime', 'SecondaryOrderID', 'LastMkt', 'Text', 'SecurityDesc',
                                      'SettlCurrency']
            self.fix_verifier.check_fix_message_fix_standard(self.execution_report,
                                                             ignored_fields=list_of_ignored_fields)
        except Exception as e:
            logger.error(f"Exception is {e}")
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule_paris)
            self.rule_manager.remove_rule(trade_rule_paris)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.disable_rule_message)
