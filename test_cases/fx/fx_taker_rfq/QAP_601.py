from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import today_front_end, tom_front_end, sn_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_601(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        tenor_today = self.data_set.get_tenor_by_name('tenor_tod')
        tenor_tom = self.data_set.get_tenor_by_name('tenor_tom')
        tenor_sn = self.data_set.get_tenor_by_name('tenor_sn')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_tenor=tenor_tom, client=client)
        self.rfq_tile.check_date(near_date=tom_front_end())
        # endregion
        # region Step 2
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_today)
        self.rfq_tile.check_date(near_date=today_front_end())
        # endregion
        # region Step 3
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_sn)
        self.rfq_tile.check_date(near_date=sn_front_end())
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
