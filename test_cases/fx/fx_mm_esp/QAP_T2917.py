from datetime import datetime
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX


class QAP_T2917(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.platinum = self.data_set.get_client_by_name("client_mm_11")
        self.eur_jpy = self.data_set.get_symbol_by_name('symbol_4')
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.eur_jpy_spot = {
            'Symbol': self.eur_jpy,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols_spot = [{
            'Instrument': self.eur_jpy_spot,
            'SettlType': self.settle_type_spot}]
        self.md_eur_jpy_spo = "EUR/JPY:SPO:REG:HSBC"
        self.md_entry_px_0 = 1.1815
        self.md_entry_px_1 = 1.18151
        self.mm_md_entry_px_0 = self.md_entry_px_0 - 0.00001
        self.mm_md_entry_px_1 = self.md_entry_px_1 + 0.00002
        self.md_entry_date = datetime.utcnow().strftime('%Y%m%d')
        self.md_entry_time = datetime.utcnow().strftime('%H:%M:%S')
        self.no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": self.md_entry_date,
                "MDEntryTime": self.md_entry_time
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.settle_date_spot,
                "MDEntryDate": self.md_entry_date,
                "MDEntryTime": self.md_entry_time
            }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step Precondition
        #  subscribing to marketdata in order to be able to set new marketdata for the instrument:
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.platinum)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data().update_MDReqID(self.md_eur_jpy_spo, self.fix_env.feed_handler, "FX")
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion
        # region Step 2-3
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.platinum)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_spot)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=self.mm_md_entry_px_0)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=self.mm_md_entry_px_1)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot, direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.fix_md.set_market_data().update_MDReqID(self.md_eur_jpy_spo, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
