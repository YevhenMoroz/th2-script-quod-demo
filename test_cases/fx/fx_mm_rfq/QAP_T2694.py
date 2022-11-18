import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2694(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.web_adm_env.session_alias_wa, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)

        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.client_tier_argentina = self.data_set.get_client_tier_id_by_name("client_tier_id_2")
        self.client_argentina = self.data_set.get_client_by_name("client_mm_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.rest_massage.find_client_tier_instrument(self.client_tier_argentina, self.eur_usd)
        params_eur_usd = self.rest_manager.send_get_request_filtered(self.rest_massage)
        params_eur_usd = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_argentina, 'instrSymbol': self.eur_usd})

        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'activeQuote', 'false', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        self.quote_request.set_swap_fwd_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                              Account=self.client_argentina)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_massage.modify_client_tier_instrument(). \
            update_value_in_component('clientTierInstrSymbolTenor', 'activeQuote', 'true', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
