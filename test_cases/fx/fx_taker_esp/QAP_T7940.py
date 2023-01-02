from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiOrderVelocityMessages import RestApiOrderVelocityMessages


class QAP_T7940(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_manager = FixManager(self.connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.connectivity, self.test_id)
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.new_order = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportAlgoFX()
        self.velocity_rule = RestApiOrderVelocityMessages()
        # region Test data
        self.symbol_for_rule = self.data_set.get_symbol_by_name("symbol_16")
        self.symbol_for_order = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.venue = self.data_set.get_venue_by_name("venue_3")
        self.market_id = self.data_set.get_market_id_by_name("market_3")

        self.client_citi = self.data_set.get_client_by_name("client_1")
        self.client_db = self.data_set.get_client_by_name("client_2")
        self.qty_for_reject = "5000000"
        self.qty_for_order = "4000000"
        self.side = "1"
        self.side_buy = "B"

        self.instrument = {
            "Symbol": self.symbol_for_order,
            "SecurityType": self.security_type
        }
        self.status_reject = Status.Reject
        self.rest_message_params = None
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.velocity_rule.set_default_params().change_params({"accountGroupID": self.client_db,
                                                               "maxCumOrdQty": self.qty_for_reject,
                                                               "instrSymbol": self.symbol_for_rule,
                                                               "side": self.side_buy}).create_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
        self.sleep(3)
        self.velocity_rule.find_all_limits()
        self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_get_request(self.velocity_rule))
        self.rest_message_params = self.rest_message_params["OrderVelocityLimitResponse"][0]
        limit_id = self.rest_message_params["orderVelocityLimitID"]
        self.sleep(5)
        # endregion

        # region Step 2
        self.new_order.set_default_SOR()
        self.new_order.change_parameters({"OrderQty": self.qty_for_order, "Account": self.client_citi,
                                          "Side": self.side})
        self.fix_manager.send_message_and_receive_response(self.new_order)
        self.execution_report.set_params_from_new_order_single(self.new_order)
        self.execution_report.change_parameters({"LastMkt": "CITI-ID", "LastQty": "*"})
        self.fix_verifier.check_fix_message(self.execution_report)
        self.sleep(3)
        # endregion
        # Region Step 3
        self.new_order.set_default_SOR()
        self.new_order.change_parameters({"OrderQty": self.qty_for_order, "Account": self.client_citi,
                                          "Side": self.side})
        self.fix_manager.send_message_and_receive_response(self.new_order)
        self.execution_report.set_params_from_new_order_single(self.new_order, status=self.status_reject)
        self.execution_report.change_parameters({"LastMkt": "CITI-ID", "LastQty": "*"})
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.velocity_rule.clear_message_params().set_params(self.rest_message_params).delete_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
