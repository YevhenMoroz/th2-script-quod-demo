from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T2816(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixQuoteRequestFX()
        self.client_tier_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.client_tier = self.data_set.get_client_by_name("client_mm_3")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.expected_notes = "request exceeds quantity threshold for instrument over this client tier"
        self.expected_quoting = "N"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_adjustment.set_defaults(). \
            update_fields_in_component("QuoteAdjustmentRequestBlock",
                                       {"InstrSymbol": self.eur_usd,
                                        "ClientTierID": self.client_tier_id})
        self.quote_adjustment.disable_pricing_by_index(1).disable_pricing_by_index(2).disable_pricing_by_index(3)
        self.java_api_manager.send_message(self.quote_adjustment)
        self.sleep(2)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.change_client(self.client_tier)
        response: list = self.java_api_manager.send_message_and_receive_response(self.quote_request, response_time=25000)
        # region Step 3
        received_notes = response[0].get_parameter("QuoteRequestNotifBlock")["FreeNotes"]
        received_quoting = response[0].get_parameter("QuoteRequestNotifBlock")["AutomaticQuoting"]
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check FreeNotes and AutomaticQuoting")
        self.verifier.compare_values("Free notes", self.expected_notes, received_notes)
        self.verifier.compare_values("AutomaticQuoting", self.expected_quoting, received_quoting)
        self.verifier.verify()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.quote_adjustment.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                        {"InstrSymbol": self.eur_usd,
                                                                         "ClientTierID": self.client_tier_id})
        self.java_api_manager.send_message(self.quote_adjustment)
        self.sleep(2)
