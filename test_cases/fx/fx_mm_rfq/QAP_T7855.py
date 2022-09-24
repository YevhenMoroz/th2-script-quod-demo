from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T7855(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_rfq_connectivity = self.fix_env.sell_side_rfq
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.free_notes_column = OrderBookColumns.free_notes.value
        self.qty_column = OrderBookColumns.qty.value
        self.client_column = QuoteRequestBookColumns.client.value
        self.presence_event = "Order presence check"
        self.expected_free_notes = "not enough quantity available through volume bands - manual intervention required"

        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.qty_5m = random_qty(4, 5, 7)
        self.qty_5m_for_dealer = random_qty(4, 5, 7)
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.instrument_spot = {"Symbol": self.gbp_usd,
                                "SecurityType": self.sec_type_spot}
        self.md_req_id = f"{self.gbp_usd}:SPO:REG:{self.hsbc}"
        self.side_sell = "2"

        self.no_md_entries_ask_more_then_bid = [
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
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.1813,
             "MDEntrySize": 3000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.1817,
             "MDEntrySize": 4000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries_ask_more_then_bid)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, OrderQty=self.qty_5m,
                                                           Account=self.iridium1, Instrument=self.instrument_spot,
                                                           Currency=self.gbp)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote_request,
                                            key_parameters=["MDReqID"])
        # endregion
        # region Step 2
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Side=self.side_sell)
        self.fix_manager_sel.send_message(self.quote_request)

        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, OrderQty=self.qty_5m_for_dealer)
        self.quote_request.remove_values_in_repeating_group_by_index("NoRelatedSymbols", 0, ("Side",))
        self.fix_manager_sel.send_message(self.quote_request)
        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.qty_5m_for_dealer, self.client_column, self.iridium1])
        actual_free_notes = self.dealer_intervention.extract_field_from_unassigned(self.free_notes_column)
        self.dealer_intervention.compare_values(self.expected_free_notes, actual_free_notes, self.presence_event)

        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.qty_5m, self.client_column, self.iridium1])
        actual_free_notes = self.dealer_intervention.extract_field_from_unassigned(self.free_notes_column)
        self.dealer_intervention.compare_values(self.expected_free_notes, actual_free_notes, self.presence_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_md.set_market_data()
        self.fix_md.update_fields_in_component("Instrument", self.instrument_spot)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
