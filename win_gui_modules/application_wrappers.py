from th2_grpc_act_gui_quod import act_ui_win_pb2


class OpenApplicationRequest:
    def __init__(self):
        self.open_application_request = act_ui_win_pb2.ApplicationDetails()

    def set_session_id(self, session_id):
        self.open_application_request.sessionID.CopyFrom(session_id)

    def set_parent_event_id(self, parent_event_id):
        self.open_application_request.parentEventId.CopyFrom(parent_event_id)

    def set_work_dir(self, work_dir: str):
        self.open_application_request.workDir = work_dir

    def set_application_file(self, app_file: str):
        self.open_application_request.applicationFile = app_file

    def build(self):
        return self.open_application_request


class LoginDetailsRequest:
    def __init__(self):
        self.login_details = act_ui_win_pb2.LoginDetails()

    def set_session_id(self, session_id):
        self.login_details.sessionID.CopyFrom(session_id)

    def set_parent_event_id(self, parent_event_id):
        self.login_details.parentEventId.CopyFrom(parent_event_id)

    def set_username(self, username: str):
        self.login_details.username = username

    def set_password(self, password: str):
        self.login_details.password = password

    def set_main_window_name(self, main_window_name: str):
        self.login_details.mainWindowName = main_window_name

    def set_login_window_name(self, login_window_name: str):
        self.login_details.loginWindowName = login_window_name

    def build(self):
        return self.login_details


class CloseApplicationRequest:
    def __init__(self):
        self.close_application_request = act_ui_win_pb2.CloseApplicationRequest()

    def set_default_params(self, base_request):
        self.close_application_request.base.CopyFrom(base_request)

    def save_workspace(self):
        self.close_application_request.saveWorkspace = True

    def build(self):
        return self.close_application_request
