from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_2774(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.beneficiary = "[Beneficiary]"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        client_1 = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile()
        self.rfq_tile.check_client_beneficiary(client=client_1, beneficiary=self.beneficiary)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
