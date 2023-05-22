import time
from datetime import datetime
from pathlib import Path
from random import randint

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
from test_framework.rest_api_wrappers.forex.RestApiPriceCleansingCrossedReferenceRatesMessages import \
    RestApiPriceCleansingCrossedReferenceRatesMessages
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile


class QAP_T9243(TestCase):
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
        self.fix_md_snapshot_doubler = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.fix_md_reject = FixMessageMarketDataRequestRejectFX()
        self.gbp_aud = self.data_set.get_symbol_by_name('symbol_9')
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_2')
        self.tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        self.settle_type = self.data_set.get_settle_type_by_name("wk1")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.instr_type_wa_spot = self.data_set.get_fx_instr_type_wa('fx_spot')
        self.instr_type_wa_fwd = self.data_set.get_fx_instr_type_wa('fx_fwd')
        self.barx = self.data_set.get_venue_by_name('venue_6')
        self.bnp = self.data_set.get_venue_by_name('venue_10')
        self.rest_message = RestApiPriceCleansingCrossedReferenceRatesMessages(data_set=self.data_set)
        self.rest_manager = RestApiManager(self.rest_env, self.test_id)
        self.rest_message_params = None
        self.instrument = {
            "Symbol": self.gbp_aud,
            "SecurityType": self.security_type,
        }
        self.instrument_eur_usd = {
            "Symbol": self.eur_usd,
            "SecurityType": self.security_type,
        }
        self.no_related_symbols = [{
            "Instrument": {
                "Symbol": self.gbp_aud,
                "CFICode": f"{self.bnp}-SW",
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
            'MarketID': f"{self.bnp}-SW"
        }]
        self.no_related_symbols_eur_usd = [{
            "Instrument": {
                "Symbol": self.eur_usd,
                "CFICode": f"{self.bnp}-SW",
                "SecurityType": self.security_type,
                "Product": "4", },
            "SettlType": self.settle_type,
            'MarketID': f"{self.bnp}-SW"
        }]

        self.md_id_bnp_fwd = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.bnp}"
        self.md_id_bnp_123_fwd = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.bnp}" + "_123"
        self.md_id_bnp_fwd_b = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.bnp}" + "_" + str(randint(100, 9999))
        self.md_id_bnp_fwd_c = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.bnp}" + "_" + str(randint(100, 9999))
        self.md_id_barx_fwd = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.barx}"
        self.md_id_barx_123_fwd = f"{self.gbp_aud}:{self.instr_type_wa_fwd}:WK1:{self.barx}" + "_123"
        self.md_id_bnp_eur_usd_fwd = f"{self.eur_usd}:{self.instr_type_wa_fwd}:WK1:{self.bnp}"
        self.md_id_bnp_eur_usd_123_fwd = f"{self.eur_usd}:{self.instr_type_wa_fwd}:WK1:{self.bnp}" + "_123"
        self.md_req_id = ''
        self.md_entries_bnp = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18118,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('wk1'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18009,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('wk1'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }
        ]
        self.md_entries_barx = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.18129,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('wk1'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.18099,
                "MDEntrySize": 1000000,
                "MDQuoteType": 1,
                "MDEntryForwardPoints": "0.0000001",
                "MDEntryPositionNo": 1,
                "SettlDate": self.data_set.get_settle_date_by_name('wk1'),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S')
            }
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Region Rule creation
        self.rest_message.set_default_params().create_cross_ref_rates_cleansing_rule().set_target_venue(
            self.bnp).set_symbol(
            self.gbp_aud).clear_ref_venues().add_ref_venue(self.barx).set_fwd()
        response = self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_multiple_request(self.rest_message))
        time.sleep(3)
        # endregion

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_bnp_123_fwd}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_id_bnp_123_fwd})
        self.fix_manager_marketdata_th2.send_message(self.md_request)

        self.fix_md.change_parameter("MDReqID", self.md_id_bnp_fwd)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries_bnp)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_bnp_fwd}")
        time.sleep(3)

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_barx_123_fwd}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_id_barx_123_fwd})
        self.fix_manager_marketdata_th2.send_message(self.md_request)

        self.fix_md.change_parameter("MDReqID", self.md_id_barx_fwd)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries_barx)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_barx_fwd}")
        time.sleep(3)

        # self.md_request.set_md_req_parameters_taker(). \
        #     change_parameters({'MDReqID': self.md_id_bnp_eur_usd_123}). \
        #     update_repeating_group("NoRelatedSymbols", self.no_related_symbols_eur_usd)
        # self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)
        #
        # self.md_request.set_md_uns_parameters_maker(). \
        #     change_parameters({'MDReqID': self.md_id_bnp_eur_usd_123})
        # self.fix_manager_marketdata_th2.send_message(self.md_request)
        #
        # self.fix_md.change_parameter("MDReqID", self.md_id_bnp_eur_usd_123)
        # self.fix_md.change_parameter("NoMDEntries", self.md_entries_bnp)
        # self.fix_md.change_parameter("Instrument", self.instrument_eur_usd)
        # self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
        #                            self.fx_fh_connectivity,
        #                            'FX')
        # self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_bnp_eur_usd}")
        # time.sleep(3)

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_bnp_fwd_b}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        fix_response = self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)[0]
        try:
            if fix_response.get_parameters()["Text"]:
                self.fix_md_reject.set_md_reject_params(self.md_request, text="suspect data").remove_parameter(
                    "MDReqRejReason")
                self.fix_verifier.check_fix_message(self.fix_md_reject)
        except KeyError:
            self.fix_md_snapshot.set_params_for_empty_md_response(self.md_request)
            self.fix_md_snapshot.add_tag({"PriceCleansingReason": "6", "OrigMDArrivalTime": "*", "OrigMDTime": "*"})
            self.fix_verifier.check_fix_message(self.fix_md_snapshot,
                                                ignored_fields=["header", "trailer", "CachedUpdate"])
        self.rest_message.clear_message_params().modify_cross_ref_rates_cleansing_rule().set_params(response)
        self.rest_message.change_params({"removeDetectedUpdate": "false"})
        self.rest_manager.send_post_request(self.rest_message)
        time.sleep(3)
        self.fix_md.change_parameter("MDReqID", self.md_id_bnp_fwd)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries_bnp)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_bnp_fwd}")
        time.sleep(3)
        self.fix_md.change_parameter("MDReqID", self.md_id_barx_fwd)
        self.fix_md.change_parameter("NoMDEntries", self.md_entries_barx)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_barx_fwd}")
        time.sleep(3)
        # endregion

        self.md_request.set_md_req_parameters_taker(). \
            change_parameters({'MDReqID': self.md_id_bnp_fwd_c}). \
            update_repeating_group("NoRelatedSymbols", self.no_related_symbols)
        self.fix_manager_marketdata_th2.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion
        # region Step 3
        self.fix_md_snapshot_doubler.set_params_for_md_response_taker_wk1(self.md_request, ["*"])
        self.fix_md_snapshot_doubler.remove_fields_in_repeating_group("NoMDEntries",
                                                                      ["MDEntryForwardPoints", "MDEntrySpotRate"])
        self.fix_md_snapshot_doubler.add_tag({'PriceCleansingReason': '6'})
        self.fix_verifier.check_fix_message(self.fix_md_snapshot_doubler,
                                            ignored_fields=["header", "trailer", "CachedUpdate"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # Deleting rule
        self.rest_message.clear_message_params().set_params(
            self.rest_message_params).delete_cross_ref_rates_cleansing_rule()
        self.rest_manager.send_post_request(self.rest_message)
        self.fix_md.set_market_data_fwd()
        self.fix_md.change_parameter("MDReqID", self.md_id_bnp_fwd)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_bnp_fwd}")
        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_req_id})
        self.fix_manager_marketdata_th2.send_message(self.md_request)
        self.fix_md.set_market_data_fwd()
        self.fix_md.change_parameter("MDReqID", self.md_id_barx_fwd)
        self.fix_md.change_parameter("Instrument", self.instrument)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_barx_fwd}")
        self.fix_md.set_market_data_fwd()
        self.fix_md.change_parameter("MDReqID", self.md_id_barx_fwd)
        self.fix_md.change_parameter("Instrument", self.instrument_eur_usd)
        self.fix_md.update_MDReqID(self.fix_md.get_parameter("MDReqID"),
                                   self.fx_fh_connectivity,
                                   'FX')
        self.fix_manager_gtw.send_message(self.fix_md, f"Send MD {self.md_id_bnp_eur_usd_fwd}")
        self.md_request.set_md_uns_parameters_maker(). \
            change_parameters({'MDReqID': self.md_req_id})
        self.fix_manager_marketdata_th2.send_message(self.md_request)
        self.sleep(4)
