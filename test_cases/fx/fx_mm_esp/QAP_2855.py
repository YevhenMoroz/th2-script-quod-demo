from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile

class QAP_2855(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

        self.ask_band = RatesColumnNames.ask_band
        self.bid_band = RatesColumnNames.bid_band

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.client = self.data_set.get_client_tier_by_name("client_tier_4")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.instrument = self.symbol + "-Spot"
        self.band_event = "band value validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)

        row_values = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=1)
        actual_bid_band = row_values[str(self.bid_band)]
        actual_ask_band = row_values[str(self.ask_band)]
        expected_bid_band = "200K"
        expected_ask_band = "200K"
        self.rates_tile.compare_values(expected_bid_band, actual_bid_band,
                                       event_name=self.band_event)
        self.rates_tile.compare_values(expected_ask_band, actual_ask_band,
                                       event_name=self.band_event)

        row_values = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=2)
        actual_bid_band = row_values[str(self.bid_band)]
        actual_ask_band = row_values[str(self.ask_band)]
        expected_bid_band = "6.2M"
        expected_ask_band = "6.2M"
        self.rates_tile.compare_values(expected_bid_band, actual_bid_band,
                                       event_name=self.band_event)
        self.rates_tile.compare_values(expected_ask_band, actual_ask_band,
                                       event_name=self.band_event)

        row_values = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=3)
        actual_bid_band = row_values[str(self.bid_band)]
        actual_ask_band = row_values[str(self.ask_band)]
        expected_bid_band = "1.2B"
        expected_ask_band = "1.2B"
        self.rates_tile.compare_values(expected_bid_band, actual_bid_band,
                                       event_name=self.band_event)
        self.rates_tile.compare_values(expected_ask_band, actual_ask_band,
                                       event_name=self.band_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
