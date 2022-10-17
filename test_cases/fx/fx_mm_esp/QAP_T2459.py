import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2459(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.nok_sek = self.data_set.get_symbol_by_name('symbol_synth_1')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_type_spot = self.data_set.get_settle_type_by_name('spot')
        self.palladium2 = self.data_set.get_client_by_name('client_mm_5')
        self.no_related_symbols_nok_sek = [{
            'Instrument': {
                'Symbol': self.nok_sek,
                'SecurityType': self.security_type_spot,
                'Product': '4', },
            'SettlType': self.settle_type_spot, }]
        self.bands_nok_sek = []
        self.no_related_symbols_eur_usd = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.security_type_spot,
                'Product': '4', },
            'SettlType': self.settle_type_spot, }]
        self.bands_eur_usd = ["1000000", '5000000', '10000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data().\
            update_value_in_repeating_group("NoMDEntries", "MDQuoteType", '0').\
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD IND")
        time.sleep(10)
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.palladium2}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_eur_usd)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_eur_usd, published=False)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        time.sleep(10)
        # endregion

        # region Step 2
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.palladium2}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_nok_sek)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        # region adapting for flexible market data
        number_of_bands = len(response[0].get_parameter("NoMDEntries")) / 2
        for i in range(int(number_of_bands)):
            self.bands_nok_sek.append("*")
        # endregion
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_nok_sek, published=False)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion

        # region Step 3
        self.fix_md.set_market_data().\
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD TRD")
        time.sleep(10)
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.palladium2}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_eur_usd)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_eur_usd)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion

        # region Step 4
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.palladium2}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_nok_sek)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_nok_sek)
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        # endregion



