import random
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import next_monday_front_end, next_working_day_after_25dec_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile

qty = str(random.randint(1000000, 2000000))
year = int(datetime.now().year)
click_to_sunday = 7 - int(datetime.now().strftime('%w'))
click_to_25dec = int(str(datetime(year, 12, 25) - datetime.now()).split()[0])


class QAP_575(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=qty, near_date=click_to_sunday,
                                                   client=client)
        self.rfq_tile.check_date(next_monday_front_end())
        # endregion
        # region Step 2
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_qty=qty, near_date=click_to_25dec,
                                                   client=client)
        self.rfq_tile.check_date(next_working_day_after_25dec_front_end())
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
