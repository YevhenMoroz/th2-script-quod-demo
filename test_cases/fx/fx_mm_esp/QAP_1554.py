import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_1554(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = SessionAliasFX().ss_esp_connectivity
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.fix_subscribe = FixMessageMarketDataRequestFX()
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_manager_fh = FixManager(self.fx_fh_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name('client_mm_4')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type = self.data_set.get_security_type_by_name('fx_spot')
        self.no_related_symbols_eur_usd = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.security_type,
                'Product': '4', },
            'SettlType': '0', }]
        self.bands_eur_usd = ["2000000", '6000000', '12000000']

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-3
        self.fix_md.set_market_data()
        self.fix_manager_fh.send_message(self.fix_md)
        time.sleep(10)
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.client}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_eur_usd)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_eur_usd)
        self.fix_md_snapshot.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        time.sleep(10)
        # endregion

        # region Step 4-5
        self.fix_md.set_market_data(). \
            update_value_in_repeating_group("NoMDEntries", "MDEntrySize", '2000000'). \
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fx_fh_connectivity, 'FX')
        self.fix_manager_fh.send_message(self.fix_md)
        time.sleep(10)
        self.fix_subscribe.set_md_req_parameters_maker(). \
            change_parameters({"SenderSubID": self.data_set.get_client_by_name('client_mm_4')}). \
            update_repeating_group('NoRelatedSymbols', self.no_related_symbols_eur_usd)
        self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, self.bands_eur_usd)
        self.fix_md_snapshot.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, 'Unsubscribe')
        time.sleep(10)
        # endregion



