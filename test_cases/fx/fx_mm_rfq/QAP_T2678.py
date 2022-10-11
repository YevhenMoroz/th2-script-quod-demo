from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from datetime import datetime
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2678(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.status = Status.Fill
        self.acc_argentina = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.qty = "1000000"
        self.buy_side = '1'
        self.sell_side = '2'

        self.offer_entry_px_1m = 1.19810
        self.bid_entry_px_1m = 1.19599
        self.spot_rate = str(round((self.bid_entry_px_1m + self.offer_entry_px_1m)/2, 5))

        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_swap
        }
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")

        self.md_symbol_spo = 'GBP/USD:SPO:REG:HSBC'
        self.md_symbol_wk1 = 'GBP/USD:FXF:WK1:HSBC'
        self.md_symbol_wk2 = 'GBP/USD:FXF:WK2:HSBC'

        self.no_md_entries_spot = [
            {
                "MDEntryType": "0",
                "MDEntryPx": self.bid_entry_px_1m,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": self.offer_entry_px_1m,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            }
        ]
        self.no_md_entries_wk1 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19585,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0002',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19615,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0002',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
        self.no_md_entries_wk2 = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19575,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0003',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19625,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntryForwardPoints": '0.0003',
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_spot)
        self.fix_md.update_MDReqID(self.md_symbol_spo, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)

        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_wk1)
        self.fix_md.update_MDReqID(self.md_symbol_wk1, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)

        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_wk2)
        self.fix_md.update_MDReqID(self.md_symbol_wk2, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
        # endregion

        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Side=self.sell_side,
                                                           Account=self.acc_argentina, Currency=self.gbp,
                                                           Instrument=self.instrument)
        self.quote_request.update_near_leg(leg_qty=self.qty, leg_side=self.buy_side, leg_symbol=self.gbp_usd)
        self.quote_request.update_far_leg(leg_qty=self.qty, leg_side=self.sell_side, leg_symbol=self.gbp_usd)
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion

        # region Step 2
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.quote.change_parameters(
            {"OfferSpotRate": self.spot_rate, "BidSpotRate": self.spot_rate})
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_symbol_spo, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)

        self.fix_md.update_MDReqID(self.md_symbol_wk1, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)

        self.fix_md.update_MDReqID(self.md_symbol_wk2, self.fh_connectivity, "FX")
        self.fix_manager_fh.send_message(self.fix_md)
