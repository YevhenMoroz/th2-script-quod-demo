from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_565(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        venue_citi = self.data_set.get_venue_by_name('venue_1')
        venue_hsbc = self.data_set.get_venue_by_name('venue_2')
        venues = [venue_citi, venue_hsbc]
        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(venue_list=venues)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
