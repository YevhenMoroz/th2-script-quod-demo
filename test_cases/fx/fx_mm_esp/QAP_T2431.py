import time
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from test_cases.fx.fx_wrapper.common_tools import add_band_tenor_lvl
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages


class QAP_T2431(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_mm = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.md_snapshot_full = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.rest_manager = RestApiManager(self.adm_env.session_alias_wa, self.test_id)
        self.rest_message = RestApiClientTierInstrSymbolMessages()
        self.client_tier_silver = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.instr_type_wa = self.data_set.get_fx_instr_type_wa('fx_spot')
        self.venue_reference = self.data_set.get_venue_by_name('venue_2')
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instrument = {
            "Symbol": self.eur_usd,
            "SecurityType": self.security_type,
        }
        self.md_id_reference = f"{self.eur_usd}:{self.instr_type_wa}:REG:{self.venue_reference}"
        self.md_entries_reference = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1815,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18151,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1813,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18165,
                "MDEntrySize": 5000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 2,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.181,
                "MDEntrySize": 10000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18186,
                "MDEntrySize": 10000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 3,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1805,
                "MDEntrySize": 15000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 4,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18196,
                "MDEntrySize": 15000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 4,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
        ]
        self.qty_list_new = ['1000000', '5000000', '10000000', '15000000']
        self.params = dict()
        self.params_default = dict()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.fix_md.set_market_data()
        self.fix_md.change_parameter("MDReqID", self.md_id_reference)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries_reference)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fx_fh_connectivity, 'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_reference}")
        time.sleep(3)
        # region Step 1-2
        self.rest_message.find_client_tier_instrument(self.client_tier_silver, self.eur_usd)
        self.params = self.rest_manager.send_get_request_filtered(self.rest_message)
        self.params = self.rest_manager. \
            parse_response_details(self.params, {'clientTierID': self.client_tier_silver, 'instrSymbol': self.eur_usd})
        self.params_default = deepcopy(self.params)
        self.params = add_band_tenor_lvl(self.params)
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params)
        self.rest_manager.send_post_request(self.rest_message)
        self.sleep(2)
        # endregion
        # region Step 3
        self.md_request.set_md_req_parameters_maker()
        response = self.fix_manager_mm.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot_full.set_params_for_md_response(self.md_request, self.qty_list_new, response=response[0])
        self.fix_verifier.check_fix_message(self.md_snapshot_full)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region 4
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_mm.send_message(self.md_request)
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            self.params_default)
        self.rest_manager.send_post_request(self.rest_message)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md)
        self.sleep(4)
        # endregion
