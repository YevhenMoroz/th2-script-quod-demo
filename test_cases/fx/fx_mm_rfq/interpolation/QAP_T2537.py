from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T2537(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_adjustment = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.quote_request = FixQuoteRequestFX()
        self.client_tier = self.data_set.get_client_by_name("client_mm_2")
        self.client_tier_id = self.data_set.get_client_tier_id_by_name("client_tier_id_2")
        self.aud_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.instr_type_spot = self.data_set.get_fx_instr_type_ja("fx_spot")
        self.instr_type_fwd = self.data_set.get_fx_instr_type_ja("fx_fwd")
        self.tenor_tom_java = self.data_set.get_tenor_java_api_by_name("tenor_tom")
        self.tenor_1w_java = self.data_set.get_tenor_java_api_by_name("tenor_1w")
        self.tenor_2w_java = self.data_set.get_tenor_java_api_by_name("tenor_2w")
        self.settle_type_tom_java = self.data_set.get_settle_type_ja_by_name("tomorrow")
        self.settle_type_1w_java = self.data_set.get_settle_type_ja_by_name("wk1")
        self.settle_type_2w_java = self.data_set.get_settle_type_ja_by_name("wk2")
        self.tenor_spot_java = self.data_set.get_tenor_java_api_by_name("tenor_spot")
        self.settle_type_spot_java = self.data_set.get_settle_type_ja_by_name("spot")
        self.expected_notes = "no forward points for client tier '2600011' on GBP/USD WK1 on QUODFX"
        self.expected_quoting = "N"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.quote_request.set_rfq_params_swap()
        self.quote_request.change_instr_symbol(self.aud_usd, self.gbp, self.usd)
        self.quote_request.change_client(self.client_tier)
        response: list = self.java_api_manager.send_message_and_receive_response(self.quote_request)
        # # region Step 3
        received_notes = response[-1].get_parameter("QuoteRequestNotifBlock")["FreeNotes"]
        received_quoting = response[-1].get_parameter("QuoteRequestNotifBlock")["AutomaticQuoting"]
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check FreeNotes and AutomaticQuoting")
        self.verifier.compare_values("Free notes", self.expected_notes, received_notes)
        self.verifier.compare_values("AutomaticQuoting", self.expected_quoting, received_quoting)
        self.verifier.verify()
        # endregion
