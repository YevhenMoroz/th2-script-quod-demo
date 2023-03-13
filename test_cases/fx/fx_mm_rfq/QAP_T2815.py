from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX


class QAP_T2815(TestCase):
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
        self.tenor_1w = self.data_set.get_tenor_java_api_by_name("tenor_1w")
        self.settle_type_1w_java = self.data_set.get_settle_type_ja_by_name("wk1")
        self.manual_request = QuoteManualSettingsRequestFX()
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.quote_adj_entry = {
            "QuoteAdjustmentEntryBlock":
                [{"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "1"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "2"},

                 {"BidMargin": "0", "OfferMargin": "0", "MDQuoteType": "IND",
                  "IndiceUpperQty": "3"}

                 ]}
        self.expected_notes = "request exceeds quantity threshold for instrument over this client tier"
        self.expected_quoting = "N"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_adjustment.set_defaults(). \
            update_fields_in_component("QuoteAdjustmentRequestBlock",
                                       {"InstrSymbol": self.eur_usd,
                                        "ClientTierID": self.client_tier_id,
                                        "Tenor": self.settle_type_1w_java,
                                        "QuoteAdjustmentEntryList": self.quote_adj_entry})
        self.java_api_manager.send_message(self.quote_adjustment)
        self.sleep(2)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.change_client(self.client_tier)
        response: list = self.java_api_manager.send_message_and_receive_response(self.quote_request, 25000)
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
                                                                         "ClientTierID": self.client_tier_id,
                                                                         "Tenor": self.settle_type_1w_java})
        self.java_api_manager.send_message(self.quote_adjustment)
        self.sleep(2)
