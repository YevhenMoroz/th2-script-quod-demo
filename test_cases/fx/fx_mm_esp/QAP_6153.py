import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_6153(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.rest_connectivity = SessionAliasFX().wa_connectivity
        self.rest_manager = RestApiManager(self.rest_connectivity, self.test_id)
        self.fix_subscribe = FixMessageMarketDataRequestFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages()
        self.init_rest_message = RestApiClientTierInstrSymbolMessages()
        self.no_related_symbols = [{
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT',
                'Product': '4', },
            'SettlType': '0', }]
        self.bands = ["1000000", '5000000', '10000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rest_massage.find_all_client_tier_instrument()
        params_eur_usd = self.rest_manager.send_get_request(self.rest_massage)
        params_eur_usd = self.rest_manager. \
            parse_response_details(
            params_eur_usd,
            {'clientTierID': '2000011', 'instrSymbol': "EUR/USD"})
        # endregion

        # region Step 2
        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'IND', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        # endregion
        time.sleep(10)
        # region Step 3
        self.fix_subscribe.set_md_req_parameters_maker().\
            change_parameters({"SenderSubID": self.data_set.get_client_by_name('client_mm_5')}).\
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands, published=False)
        time.sleep(5)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region Postconditions
        self.rest_massage.modify_client_tier_instrument(). \
                update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'TRD', {'tenor': 'SPO'})
        self.rest_manager.send_post_request(self.rest_massage)
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion

    # @try_except
    # def run_post_conditions(self):
    #     self.rest_massage.modify_client_tier_instrument(). \
    #         update_value_in_component('clientTierInstrSymbolTenor', 'MDQuoteType', 'TRD', {'tenor': 'SPO'})
    #     self.rest_manager.send_post_request(self.rest_massage)
    #     self.fix_subscribe.set_md_uns_parameters_maker()
    #     self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')


