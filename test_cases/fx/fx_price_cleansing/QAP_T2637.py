import time
from datetime import datetime
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.DataSet import DirectionEnum

from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from custom import basic_custom_actions as bca
from test_framework.rest_api_wrappers.forex.RestApiPriceCleansingStaleRatesMessages import \
    RestApiPriceCleansingStaleRatesMessages
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile


class QAP_T2637(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fx_fh_connectivity = SessionAliasFX().fx_fh_connectivity
        self.rest_connectivity = SessionAliasFX().wa_connectivity
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_env = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_manager_gtw = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_marketdata_th2 = FixManager(self.fix_env.buy_side_md, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.buy_side_md, self.test_id)
        self.rates_tile = RatesTile(self.test_id, self.session_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.md_reject = FixMessageMarketDataRequestRejectFX()
        self.symbol = self.data_set.get_symbol_by_name('symbol_2')
        self.tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        self.settle_type = self.data_set.get_settle_type_by_name("spot")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.instr_type_wa = self.data_set.get_fx_instr_type_wa('fx_spot')
        self.venue = self.data_set.get_venue_by_name('venue_8')
        self.rest_message = RestApiPriceCleansingStaleRatesMessages(data_set=self.data_set)
        self.rest_manager = RestApiManager(self.rest_env, self.test_id)
        self.rest_message_params = None
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type,
        }
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.symbol,
                "CFICode": f"{self.venue}-SW",
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
            'MarketID': f"{self.venue}-SW"
        }]
        self.md_id_citi = f"{self.symbol}:{self.instr_type_wa}:REG:{self.venue}"
        self.md_id_citi_123 = f"{self.symbol}:{self.instr_type_wa}:REG:{self.venue}"+"_123"
        self.md_req_id = ''
        self.md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": round(1.18138, 5),
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18158,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('spot'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Region Rule creation
        self.rest_message.set_default_params().create_stale_cleansing_rule().set_venue(self.venue).set_symbol(
            self.symbol)
        self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_multiple_request(self.rest_message))
        time.sleep(3)
        # endregion

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_citi_123}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_id_citi_123})
        self.fix_manager_marketdata_th2.send_message(self.md_request)

        self.fix_md.change_parameter("MDReqID", self.md_id_citi)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_citi}")
        time.sleep(3)

        self.fix_md.change_parameter("MDReqID", self.md_id_citi)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.md_req_id = self.fix_md.get_parameter("MDReqID")

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_req_id}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3
        self.md_reject.set_md_reject_params(self.md_request, text="feed stale").remove_parameter("MDReqRejReason")
        self.fix_verifier.check_fix_message(fix_message=self.md_reject,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.rest_message.clear_message_params().set_params(self.rest_message_params).delete_stale_cleansing_rule()
        self.rest_manager.send_post_request(self.rest_message)
        self.fix_md.set_market_data()
        self.fix_md.change_parameter("MDReqID", self.md_id_citi)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_citi}")
        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_req_id})
        self.fix_manager_marketdata_th2.send_message(self.md_request)
        self.sleep(2)
