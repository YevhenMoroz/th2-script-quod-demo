from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T2989(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.quote_request_book = FXQuoteRequestBook(self.test_id, self.session_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)
        self.qty = '10000000'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        aud_currency = self.data_set.get_currency_by_name('currency_aud')
        aud_brl_symbol = self.data_set.get_symbol_by_name('symbol_ndf_3')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')

        # region Step 1
        self.rfq_tile.crete_tile()
        self.rfq_tile.check_currency_pair(currency_pair=aud_brl_symbol)
        # endregion
        # region Step 2
        self.rfq_tile.check_qty(near_qty=self.qty)
        # endregion
        # region Step 3
        self.rfq_tile.check_tenor(near_tenor=near_tenor)
        # endregion
        # region Step 4
        self.rfq_tile.check_date(near_date=spo_front_end())
        # endregion
        # region Step 5
        self.rfq_tile.check_labels(left_label='Sell AUD', right_label='Buy AUD')
        # endregion
        # region Step 6
        self.rfq_tile.check_currency(currency=aud_currency)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
