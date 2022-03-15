from typing import List

from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.environments.fe_environment import FEEnvironment
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.utils import prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base


class BaseMainWindow(BaseWindow):

    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.case_id = case_id
        self.session_id = session_id

    # endregion

    def open_fe(self, report_id, fe_env: FEEnvironment, user_num=1, is_open=True):
        init_event = create_event("Initialization", parent_id=report_id)
        set_base(self.session_id, self.case_id)
        if not is_open:
            username = 'fe_env.user_' + str(user_num)
            password = 'fe_env.password_' + str(user_num)
            prepare_fe(init_event, self.session_id, fe_env.folder, eval(username), eval(password), fe_env.main_window,
                       fe_env.login_window, fe_env.exe_name)
        else:
            get_opened_fe(self.case_id, self.session_id, fe_env.main_window)

    def switch_user(self):
        search_fe_req = FEDetailsRequest()
        search_fe_req.set_session_id(self.session_id)
        search_fe_req.set_parent_event_id(self.case_id)
        Stubs.win_act.moveToActiveFE(search_fe_req.build())
        set_base(self.session_id, self.case_id)
