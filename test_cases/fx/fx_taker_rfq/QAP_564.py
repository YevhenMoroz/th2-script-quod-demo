from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end, wk1_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile

qty = '10000000'
qty1 = '1m'
qty_1m = '1000000'
qty2 = '100k'
qty_100k = '100000'
usd_label_left = 'Buy USD'
usd_label_right = 'Sell USD'


class QAP_564(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        near_tenor_1 = self.data_set.get_tenor_by_name('tenor_spot')
        near_tenor_2 = self.data_set.get_tenor_by_name('tenor_1w')
        client = self.data_set.get_client_by_name("client_1")
        venue = self.data_set.get_venue_by_name('venue_1')

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=qty, near_tenor=near_tenor_1,
                                                   client=client, single_venue=venue)
        # region Step 2
        self.rfq_tile.check_currency_pair(currency_pair=eur_usd_symbol)
        # endregion
        # region Step 3
        self.rfq_tile.check_date(near_date=spo_front_end())
        # endregion
        # region Step 4
        self.rfq_tile.crete_tile().modify_rfq_tile(change_currency=True)
        self.rfq_tile.check_labels(left_label=usd_label_left, right_label=usd_label_right)
        # endregion
        # region Step 5
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=qty1)
        self.rfq_tile.check_qty(near_qty=qty_1m)
        # endregion
        # region Step 6
        self.rfq_tile.crete_tile().modify_rfq_tile(near_qty=qty2)
        self.rfq_tile.check_qty(near_qty=qty_100k)
        # endregion
        # region Step 7
        self.rfq_tile.crete_tile().modify_rfq_tile(near_tenor=near_tenor_2)
        self.rfq_tile.check_date(near_date=wk1_front_end())
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
