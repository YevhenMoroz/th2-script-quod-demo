from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_7556(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.web_adm_env.session_alias_wa, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)

        self.gbp_aud = self.data_set.get_symbol_by_name('symbol_9')
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.client_tier_iridium = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.client_iridium = self.data_set.get_client_by_name("client_mm_3")

        self.instrument_gbp_aud = {
            "Symbol": self.gbp_aud,
            "SecurityType": self.security_type_spot}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                            Account=self.client_iridium,
                                                                            Currency=self.gbp,
                                                                            Instrument=self.instrument_gbp_aud)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote)
        # endregion

        # region Step 2
        self.rest_massage.find_all_client_tier_instrument()
        params_gbp_aud = self.rest_manager.send_get_request(self.rest_massage)
        params_gbp_aud = self.rest_manager. \
            parse_response_details(params_gbp_aud,
                                   {'clientTierID': self.client_tier_iridium, 'instrSymbol': self.gbp_aud})

        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_gbp_aud). \
            update_value_in_component('clientTierInstrSymbolVenue', 'excludeWhenUnhealthy', 'true', {'venueID': 'BNP'})
        self.rest_manager.send_post_request(self.rest_massage)

        quote_cancel = FixMessageQuoteCancelFX().set_params_for_receive(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote_cancel, key_parameters=["QuoteReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_massage.modify_client_tier_instrument(). \
            update_value_in_component('clientTierInstrSymbolVenue', 'excludeWhenUnhealthy', 'false', {'venueID': 'BNP'})
        self.rest_manager.send_post_request(self.rest_massage)