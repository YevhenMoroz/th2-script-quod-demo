from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_2345(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.acc_palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.jpy = self.data_set.get_currency_by_name("currency_jpy")

        self.fx_fh_q_connectivity = self.fix_env.feed_handler2
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_q_connectivity, self.test_id)

        self.qty_3m = "3000000"
        self.bid_px_ccy1 = '104.63'
        self.offer_px_ccy1 = '104.635'
        self.bid_px_ccy2 = '104.632'
        self.offer_px_ccy2 = '104.633'
        self.instrument = {"Symbol": "USD/JPY",
                           "SecurityType": "FXSPOT"}
        self.md_req_id = 'USD/JPY:SPO:REG:CITI'
        self.correct_no_md_entries = [
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

        self.incorrect_no_md_entries = [
            {
                "MDEntryType": "0",
                "MDEntryPx": 104.632,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_1w,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 104.633,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                'SettlDate': self.settle_date_1w,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "0",
                "MDEntryPx": 104.630,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_1w,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 104.635,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
                'SettlDate': self.settle_date_1w,
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },

        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Instrument=self.instrument,
                                                           Account=self.acc_palladium1)
        self.fix_manager.send_message_and_receive_response(self.quote_request,
                                                           self.test_id)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument)
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_q_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument)
        self.fix_md.update_repeating_group("NoMDEntries", self.incorrect_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_q_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.quote_cancel.set_params_for_receive(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote_cancel, key_parameters=["QuoteReqID"])
