import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6976(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.mic = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.minor_currency = self.data_set.get_currency_by_name("currency_3")
        self.fix_message.change_parameters({"ExDestination": self.mic, "SettlCurrency": self.minor_currency})
        self.fix_message.remove_parameter("Currency")
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_2')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.currency = self.data_set.get_currency_by_name("currency_2")
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.mod_inst = RestApiModifyInstitutionMessage(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.mod_inst.change_params({"crossCurrencySettlement": False})
        self.rest_api_manager.send_post_request(self.mod_inst)
        time.sleep(5)
        # endregion
        # region Step 1
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, int(self.price),
                                                                                          int(self.qty), 0)
            self.fix_message.change_parameter("Account", self.client)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"SettlCurrency": self.currency}, exec_rep, "Check major currency")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.mod_inst.change_params({"crossCurrencySettlement": True})
        self.rest_api_manager.send_post_request(self.mod_inst)
