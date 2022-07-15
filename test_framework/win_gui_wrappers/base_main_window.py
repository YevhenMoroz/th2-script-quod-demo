from typing import List

from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.environments.fe_environment import FEEnvironment
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.application_wrappers import FEDetailsRequest, PanicDetails
from win_gui_modules.layout_panel_wrappers import WorkspaceModificationRequest
from win_gui_modules.utils import prepare_fe, get_opened_fe, close_fe, call
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

    def close_fe(self):
        close_fe(self.case_id, self.session_id)

    def import_layout(self, path, file_name):
        ws_modify_req = WorkspaceModificationRequest()
        ws_modify_req.set_default_params(self.base_request)
        ws_modify_req.do_import()
        ws_modify_req.set_path(path)
        ws_modify_req.set_filename(file_name)
        call(Stubs.win_act_options.modifyWorkspace, ws_modify_req.build())

    def export_layout(self, path, file_name):
        ws_modify_req = WorkspaceModificationRequest()
        ws_modify_req.set_default_params(self.base_request)
        ws_modify_req.do_export()
        ws_modify_req.set_path(path)
        ws_modify_req.set_filename(file_name)
        call(Stubs.win_act_options.modifyWorkspace, ws_modify_req.build())

    def reset_layout(self):
        call(Stubs.win_act_options.resetWorkspace, self.base_request)

    def panic(self, start_time=None, end_time=None, listing=None, sub_venue=None, venue=None, client=None,
              instrument=None, status=None, tif=None, exec_status=None, side=None, extract_footer=False):
        panic_details = PanicDetails(self.base_request)
        panic_details.set_start_time(start_time)
        panic_details.set_end_time(end_time)
        panic_details.set_listing(listing)
        panic_details.set_sub_venue(sub_venue)
        panic_details.set_venue(venue)
        panic_details.set_client(client)
        panic_details.set_instrument(instrument)
        panic_details.set_status(status)
        panic_details.set_tif(tif)
        panic_details.set_exec_status(exec_status)
        panic_details.set_side(side)
        panic_details.extract_footer(extract_footer)
        result = call(Stubs.win_act.panicAction, panic_details.build())
        self.clear_details([panic_details])
        return result
