import time
from pathlib import Path
from datetime import datetime
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


class QAP_T5995(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)

        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_date_1w = self.data_set.get_settle_date_by_name("spo_ndf")
        self.acc_argentina = self.data_set.get_client_by_name("client_mm_2")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.sec_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.ms = self.data_set.get_venue_by_name("venue_3")
        self.instrument_swap = {"Symbol": self.eur_usd,
                                "SecurityType": self.sec_type_swap}
        self.instrument_spot = {"Symbol": self.eur_usd,
                                "SecurityType": self.sec_type_spot}
        self.md_req_id = f"{self.eur_usd}:SPO:REG:{self.ms}"

        self.correct_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.1815,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.18151,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.incorrect_no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 104.642,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_1w,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 104.643,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_1w,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

        self.no_related_symbols_eur_usd = [{
            'Instrument': {
                'Symbol': self.eur_usd,
                'SecurityType': self.sec_type_spot,
                'Product': '4', },
            'SettlType': '0', }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Instrument=self.instrument_swap,
                                                           Account=self.acc_argentina)
        self.fix_manager.send_message_and_receive_response(self.quote_request,
                                                           self.test_id)
        # region Step 1
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.correct_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)

        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])

        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Instrument=self.instrument_swap,
                                                           Account=self.acc_argentina)
        self.fix_manager.send_message_and_receive_response(self.quote_request,
                                                           self.test_id)

        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.incorrect_no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        time.sleep(10)

        self.quote_cancel.set_params_for_receive(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote_cancel, key_parameters=["QuoteReqID"])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
