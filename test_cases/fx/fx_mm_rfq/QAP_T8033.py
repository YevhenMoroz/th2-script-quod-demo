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
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T8033(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.modify_instrument = RestApiClientTierInstrSymbolMessages()
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.params_eur_usd = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        self.text = "subscriptions on this tier/tenor is not currently allowed"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.client,
                                                           Currency="GBP", Instrument=self.instrument)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.rest_massage.find_client_tier_instrument(self.client_id, self.gbp_usd)
        # endregion
        # region Step 1
        self.params_eur_usd = self.rest_manager.send_get_request_filtered(self.rest_massage)
        self.params_eur_usd = self.rest_manager. \
            parse_response_details(self.params_eur_usd,
                                   {'clientTierID': self.client_id, 'instrSymbol': self.gbp_usd})

        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(self.params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'IND', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        # endregion
        # region Step 3
        quote_cancel = FixMessageQuoteCancelFX().set_params_for_receive(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote_cancel, key_parameters=["QuoteReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(self.params_eur_usd) \
            .update_value_in_component("clientTierInstrSymbolTenor", "MDQuoteType", "TRD")
        self.rest_manager.send_post_request(self.modify_instrument)
        self.sleep(2)
