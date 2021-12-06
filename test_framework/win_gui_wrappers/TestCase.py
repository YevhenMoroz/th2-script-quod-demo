import os
from custom import basic_custom_actions as bca
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base


class TestCase:
    def __init__(self, report_id, session_id):
        self.session_id = session_id
        self.report_id = report_id
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        set_base(self.session_id, self.test_id)
        self.base_request = get_base_request(session_id, self.test_id)
        self.ss_connectivity = None
        self.bs_connectivity = None
        self.dc_connectivity = None
        self.wa_connectivity = None
