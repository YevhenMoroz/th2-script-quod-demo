from common import config_vars
from utils.application_wrappers import CloseApplicationRequest, OpenApplicationRequest, LoginDetailsRequest
from utils.base_test import BaseTest
from utils.layout_panel_wrappers import WorkspaceModificationRequest
from utils.services import Services
from utils.wrappers import *


class QAP_2726(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event,
                               "QAP_2726", "Verify that parent filter in Order Book is not applied to child orders")

    def execute(self):
        call = self.call
        set_base(self._session_id, self._event_id)

        act = self._services.layout_panel_service

        # action to import/export workspace
        ws_modify_req = WorkspaceModificationRequest()
        ws_modify_req.set_default_params(self.get_base_request())
        ws_modify_req.do_import()  # / ws_modify_req.do_export()
        ws_modify_req.set_path("C:\QUOD305")
        ws_modify_req.set_filename("Workspace1.xml")
        call(act.modifyWorkspace, ws_modify_req.build())

        # action to save workspace when closing the application
        app_service = self._services.main_win_service
        close_app_request = CloseApplicationRequest()
        close_app_request.set_default_params(self.get_base_request())
        close_app_request.save_workspace()
        app_service.closeApplication(close_app_request.build())

        # action to open app
        open_app_req = OpenApplicationRequest()
        open_app_req.set_session_id(self._session_id)
        open_app_req.set_parent_event_id(self._event_id)
        open_app_req.set_work_dir(config_vars.qf_trading_fe_folder)
        open_app_req.set_application_file(config_vars.qf_trading_fe_exec)
        app_service.openApplication(open_app_req.build())

        # action to login
        login_details_req = LoginDetailsRequest()
        login_details_req.set_session_id(self._session_id)
        login_details_req.set_parent_event_id(self._event_id)
        login_details_req.set_username(config_vars.qf_trading_fe_user)
        login_details_req.set_password(config_vars.qf_trading_fe_password)
        login_details_req.set_main_window_name(config_vars.qf_trading_fe_main_win_name)
        login_details_req.set_login_window_name(config_vars.qf_trading_fe_login_win_name)
        app_service.login(login_details_req.build())
