from pathlib import Path
from datetime import datetime

from decimal import *

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2836(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()

        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.acc_palladium1 = self.data_set.get_client_by_name("client_mm_2")
        self.jpy = self.data_set.get_currency_by_name("currency_usd")
        self.usd = self.data_set.get_currency_by_name("currency_eur")
        self.usd_jpy = self.data_set.get_symbol_by_name("symbol_1")

        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)

        self.qty_3m = "3000000"
        self.bid_px_ccy1 = "104.6325"
        self.offer_px_ccy1 = "104.6325"
        self.bid_px_ccy2 = "104.6325"
        self.off_px_ccy2 = "104.6325"
        self.instrument_spot = {"Symbol": self.usd_jpy,
                                "SecurityType": "FXSPOT"}
        self.instrument_swap = {"Symbol": self.usd_jpy,
                                "SecurityType": "FXSWAP"}
        self.md_req_id = 'EUR/USD:SPO:REG:MS'
        self.no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 104.632,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 104.633,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 104.630,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 104.635,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },

        ]
        self.response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Instrument=self.instrument_swap,
                                                           Account=self.acc_palladium1,
                                                           Currency=self.jpy)
        self.quote_request.update_near_leg(leg_qty=self.qty_3m, leg_symbol=self.usd_jpy)
        self.quote_request.update_far_leg(leg_qty=self.qty_3m, leg_symbol=self.usd_jpy)
        self.response = self.fix_manager.send_message_and_receive_response(self.quote_request,
                                                           self.test_id)
        bid_fwd_pts = self.response[0].get_parameter("NoLegs")[1]["LegBidForwardPoints"]
        self.bid_px_ccy2 = str(round(Decimal(float(self.bid_px_ccy2)) + Decimal(float(bid_fwd_pts)), 6))
        self.quote.set_params_for_quote_swap_ccy2(self.quote_request, near_leg_off_px=self.off_px_ccy2,
                                                  far_leg_bid_px=self.bid_px_ccy2)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])

        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager.send_message(self.quote_cancel)
        # endregion

        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Instrument=self.instrument_swap,
                                                           Account=self.acc_palladium1,
                                                           Currency=self.usd)
        self.quote_request.update_near_leg(leg_qty=self.qty_3m, leg_symbol=self.usd_jpy)
        self.quote_request.update_far_leg(leg_qty=self.qty_3m, leg_symbol=self.usd_jpy)

        self.response = self.fix_manager.send_message_and_receive_response(self.quote_request,
                                                           self.test_id)
        ask_fwd_pts = self.response[0].get_parameter("NoLegs")[1]["LegOfferForwardPoints"]
        self.offer_px_ccy1 = str(round(Decimal(float(self.offer_px_ccy1)) + Decimal(float(ask_fwd_pts)), 6))
        self.quote.set_params_for_quote_swap(self.quote_request, near_leg_bid_px=self.bid_px_ccy1,
                                             far_leg_off_px=self.offer_px_ccy1)
        self.quote.remove_parameters(["BidSwapPoints", "BidPx"])
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager.send_message(self.quote_cancel)
        self.sleep(2)
