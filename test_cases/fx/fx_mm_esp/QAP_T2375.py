from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2375(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_esp_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.modify_instrument = RestApiClientTierInstrSymbolMessages()
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.ss_esp_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_esp_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.client_id = self.data_set.get_client_tier_id_by_name("client_tier_id_7")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.usd_cad = self.data_set.get_symbol_by_name("symbol_12")
        self.gbp_cad = self.data_set.get_symbol_by_name("symbol_synth_5")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.msg_prams_instr_gbp_usd = None
        self.msg_prams_instr_usd_cad = None
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.gbp_cad,
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type, }]
        self.bands_gbp_usd = ["1000000"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.modify_instrument.find_client_tier_instrument(self.client_id, self.gbp_usd)
        self.msg_prams_instr_gbp_usd = self.rest_manager.send_get_request_filtered(self.modify_instrument)
        self.msg_prams_instr_gbp_usd = self.rest_manager. \
            parse_response_details(self.msg_prams_instr_gbp_usd,
                                   {"clientTierID": self.client_id, "instrSymbol": self.gbp_usd})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(
            self.msg_prams_instr_gbp_usd) \
            .update_value_in_component("clientTierInstrSymbolTenor", "allowQuoteRequests", "false")
        self.modify_instrument.update_value_in_component("clientTierInstrSymbolTenor", "allowESPSubscriptions", "false")
        self.rest_manager.send_post_request(self.modify_instrument)
        self.modify_instrument.find_client_tier_instrument(self.client_id, self.usd_cad)
        self.msg_prams_instr_usd_cad = self.rest_manager.send_get_request_filtered(self.modify_instrument)
        self.msg_prams_instr_usd_cad = self.rest_manager. \
            parse_response_details(self.msg_prams_instr_usd_cad,
                                   {"clientTierID": self.client_id, "instrSymbol": self.usd_cad})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(
            self.msg_prams_instr_usd_cad) \
            .update_value_in_component("clientTierInstrSymbolTenor", "allowQuoteRequests", "false")
        self.modify_instrument.update_value_in_component("clientTierInstrSymbolTenor", "allowESPSubscriptions", "false")
        self.rest_manager.send_post_request(self.modify_instrument)
        self.sleep(5)
        # endregion
        # region Step 2
        self.md_request.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3
        self.md_request.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.md_request, self.bands_gbp_usd)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot, key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager.send_message(self.md_request, "Unsubscribe")
        # endregion

        # region Step 4
        self.modify_instrument.find_client_tier_instrument(self.client_id, self.gbp_usd)
        self.msg_prams_instr_gbp_usd = self.rest_manager.send_get_request_filtered(self.modify_instrument)
        self.msg_prams_instr_gbp_usd = self.rest_manager. \
            parse_response_details(self.msg_prams_instr_gbp_usd,
                                   {"clientTierID": self.client_id, "instrSymbol": self.gbp_usd})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(
            self.msg_prams_instr_gbp_usd) \
            .update_value_in_component("clientTierInstrSymbolTenor", "allowQuoteRequests", "true")
        self.modify_instrument.update_value_in_component("clientTierInstrSymbolTenor", "allowESPSubscriptions", "true")
        self.rest_manager.send_post_request(self.modify_instrument)
        self.modify_instrument.find_client_tier_instrument(self.client_id, self.usd_cad)
        self.msg_prams_instr_usd_cad = self.rest_manager.send_get_request_filtered(self.modify_instrument)
        self.msg_prams_instr_usd_cad = self.rest_manager. \
            parse_response_details(self.msg_prams_instr_usd_cad,
                                   {"clientTierID": self.client_id, "instrSymbol": self.usd_cad})
        self.modify_instrument.clear_message_params().modify_client_tier_instrument().set_params(
            self.msg_prams_instr_usd_cad) \
            .update_value_in_component("clientTierInstrSymbolTenor", "allowQuoteRequests", "true")
        self.modify_instrument.update_value_in_component("clientTierInstrSymbolTenor", "allowESPSubscriptions", "true")
        self.rest_manager.send_post_request(self.modify_instrument)
        self.sleep(5)
        # endregion
        # region Step 5
        self.md_request.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.md_request, self.bands_gbp_usd)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot, key_parameters=["MDReqID"])
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager.send_message(self.md_request, "Unsubscribe")
        # endregion

