from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_3234(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        # self.fx_fh_q_connectivity = self.fix_env.feed_handler2
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_fh_314 = FixManager(self.fix_env.feed_handler2, self.test_id)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)

        self.eur_gbp = self.data_set.get_symbol_by_name('symbol_3')
        self.eur = self.data_set.get_currency_by_name("currency_eur")
        self.client_tier_iridium = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.client_iridium = self.data_set.get_client_by_name("client_mm_3")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')

        self.md_req_id = 'EUR/USD:SPO:REG:HSBC'
        self.no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19585,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19612,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19584,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19615,
                "MDEntrySize": 6000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19581,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19620,
                "MDEntrySize": 12000000,
                "MDEntryPositionNo": 3,
                'SettlDate': self.settle_date_spot,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        # self.fix_md.update_MDReqID(self.md_req_id, self.fix_env.feed_handler2, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        # endregion

        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion

        # region Step 2
        quote = FixMessageQuoteFX().set_params_for_quote_swap(self.quote_request)
        quote.change_parameters({"BidSpotRate": "1.19599", "OfferSpotRate": "1.19599"})
        self.fix_verifier.check_fix_message(fix_message=quote)
        # endregion
