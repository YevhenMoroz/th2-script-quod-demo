from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, TriggerType, OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_order_ticket import FXOrderTicket
from test_framework.win_gui_wrappers.forex.rates_tile import RatesTile


class QAP_3636(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = RatesTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.order_ticket = FXOrderTicket(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.feed_handler, self.test_id)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshBuyFX()

        self.symbol = self.data_set.get_symbol_by_name("symbol_8")
        self.tenor_spot = self.data_set.get_tenor_by_name("tenor_spot")
        self.client = self.data_set.get_client_by_name("client_1")
        self.tif = TimeInForce.GTC.value
        self.trigger_type = TriggerType.market_best_bid_offer
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.md_symbol = self.symbol + ":SPO:REG:" + self.venue
        self.qty_col = OrderBookColumns.qty.value
        self.stp_px_col = OrderBookColumns.stop_price.value
        self.sts_coll = OrderBookColumns.sts.value
        self.open_sts = ExecSts.open.value
        self.term_sts = ExecSts.terminated.value
        self.from_cur = self.symbol[:3]
        self.to_cur = self.symbol[4:]
        self.qty = random_qty(4, 5, 7)
        self.order_price_buy = "1.19"
        self.order_price_sell = "1.17"
        self.stop_price1 = "1.1812"
        self.md_px1 = "1.1813"
        self.md_px2 = "1.183"
        self.md_px3 = "1.1805"
        self.stop_price2 = "1.182"
        self.stop_price3 = "1.184"
        self.stop_price4 = "1.181"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send MD
        self.md_snapshot.set_market_data()
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=self.md_px1)
        self.md_snapshot.update_MDReqID(self.md_symbol, self.fix_env.feed_handler, "FX")
        self.fix_manager.send_message(self.md_snapshot, "Send MD to USD/SEK")
        # endregion
        # region Step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_rates_tile(self.from_cur, self.to_cur, self.tenor_spot, qty=self.qty)
        self.rates_tile.click_on_tob_buy()
        self.order_ticket.set_order_details(tif=self.tif, stop_price=self.stop_price1, price_large=self.order_price_buy,
                                            client=self.client)
        self.order_ticket.add_synth_ord_type_str(self.trigger_type)
        self.order_ticket.create_order()
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price1, self.sts_coll: self.term_sts})
        # endregion
        # region Step 2
        self.rates_tile.modify_rates_tile(self.from_cur, self.to_cur, self.tenor_spot, qty=self.qty)
        self.rates_tile.click_on_tob_buy()
        self.order_ticket.set_order_details(tif=self.tif, stop_price=self.stop_price2, price_large=self.order_price_buy,
                                            client=self.client)
        self.order_ticket.add_synth_ord_type_str(self.trigger_type)
        self.order_ticket.create_order()
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price2, self.sts_coll: self.open_sts})
        self.md_snapshot.set_market_data()
        self.md_snapshot.update_value_in_repeating_group("NoMDEntries", "MDEntryPx", self.md_px2)
        self.md_snapshot.update_MDReqID(self.md_symbol, self.fix_env.feed_handler, "FX")
        self.fix_manager.send_message(self.md_snapshot, "Send MD to USD/SEK")
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price2, self.sts_coll: self.term_sts})
        # endregion
        # region step 3
        self.rates_tile.click_on_tob_sell()
        self.order_ticket.set_order_details(tif=self.tif, stop_price=self.stop_price3,
                                            price_large=self.order_price_sell,
                                            client=self.client)
        self.order_ticket.add_synth_ord_type_str(self.trigger_type)
        self.order_ticket.create_order()
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price3, self.sts_coll: self.term_sts})
        # endregion
        # region Step 4
        self.rates_tile.click_on_tob_sell()
        self.order_ticket.set_order_details(tif=self.tif, stop_price=self.stop_price4,
                                            price_large=self.order_price_sell,
                                            client=self.client)
        self.order_ticket.add_synth_ord_type_str(self.trigger_type)
        self.order_ticket.create_order()
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price4, self.sts_coll: self.open_sts})
        self.md_snapshot.set_market_data()
        self.md_snapshot.update_value_in_repeating_group("NoMDEntries", "MDEntryPx", self.md_px3)
        self.md_snapshot.update_MDReqID(self.md_symbol, self.fix_env.feed_handler, "FX")
        self.fix_manager.send_message(self.md_snapshot, "Send MD to USD/SEK")
        self.order_book.set_filter([self.qty_col, self.qty]).check_order_fields_list(
            {self.stp_px_col: self.stop_price4, self.sts_coll: self.term_sts})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Restore MD
        self.md_snapshot.set_market_data()
        self.md_snapshot.update_MDReqID(self.md_symbol, self.fix_env.feed_handler, "FX")
        self.fix_manager.send_message(self.md_snapshot, "Send MD to USD/SEK")
        # endregion

