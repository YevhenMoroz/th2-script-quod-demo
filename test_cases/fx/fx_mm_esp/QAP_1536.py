from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames, ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileValues

ask_band = RatesColumnNames.ask_band
bid_band = RatesColumnNames.bid_band


class QAP_1536(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol1 = self.data_set.get_symbol_by_name("symbol_1")
        # I've picked a symbol that is not present in silver client tier for now:
        self.symbol5 = self.data_set.get_symbol_by_name("symbol_5")
        self.instrument1 = self.symbol1 + "-Spot"
        self.instrument2 = self.symbol5 + "-Spot"

        self.now = datetime.now()
        self.date = spo_front_end()


        self.instrument_event = "instrument validation"
        self.client_tier_event = "client_tier validation"
        self.date_event = "date validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):



        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument1, client_tier=self.client)
        # endregion

        # region step 2
        header_values = self.rates_tile.extract_header(instrument="instrument", client_tier="client_tier", date="date")
        actual_instrument1 = header_values["instrument"]
        actual_client_tier1 = header_values["client_tier"]
        extracted_date_value = header_values["date"]
        fedate = extracted_date_value + "-" + str(self.now.year)
        actual_date1 = datetime.strptime(fedate, "%d-%b-%Y").strftime('%Y-%m-%d %H:%M:%S')
        self.rates_tile.compare_values(self.instrument1, actual_instrument1,
                                       event_name=self.instrument_event)
        self.rates_tile.compare_values(self.date, actual_date1,
                                       event_name=self.date_event)
        self.rates_tile.compare_values(self.client, actual_client_tier1,
                                       event_name=self.client_tier_event)
        # endregion

        # region step 3
        self.rates_tile.modify_client_tile(instrument=self.instrument2)
        header_values = self.rates_tile.extract_header(instrument="instrument", client_tier="client_tier", date="date")
        actual_instrument1 = header_values["instrument"]
        actual_client_tier1 = header_values["client_tier"]
        extracted_date_value = header_values["date"]
        fedate = extracted_date_value + "-" + str(self.now.year)
        actual_date1 = datetime.strptime(fedate, "%d-%b-%Y").strftime('%Y-%m-%d %H:%M:%S')
        self.rates_tile.compare_values(self.instrument1, actual_instrument1,
                                       event_name=self.instrument_event)
        self.rates_tile.compare_values(self.date, actual_date1,
                                       event_name=self.date_event)
        self.rates_tile.compare_values(self.client, actual_client_tier1,
                                       event_name=self.client_tier_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
