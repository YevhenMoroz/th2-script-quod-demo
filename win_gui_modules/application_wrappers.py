from th2_grpc_act_gui_quod import act_ui_win_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest


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

    def is_error_expected(self, is_error_expected: bool):
        self.login_details.isErrorExpected = is_error_expected

    def set_extraction_id(self, extraction_id: str):
        self.login_details.extractionId = extraction_id

    def close_login_windows(self):
        self.login_details.closeLoginWindow = True

    def build(self):
        return self.login_details

class FEDetailsRequest:
    def __init__(self):
        self.fe_details = act_ui_win_pb2.FEDetails()

    def set_session_id(self, session_id):
        self.fe_details.sessionID.CopyFrom(session_id)

    def set_parent_event_id(self, parent_event_id):
        self.fe_details.parentEventId.CopyFrom(parent_event_id)

    def set_main_window_name(self, main_window_name: str):
        self.fe_details.mainWindowName = main_window_name

    def build(self):
        return self.fe_details


class CloseApplicationRequest:
    def __init__(self):
        self.close_application_request = act_ui_win_pb2.CloseApplicationRequest()

    def set_default_params(self, base_request):
        self.close_application_request.base.CopyFrom(base_request)

    def save_workspace(self):
        self.close_application_request.saveWorkspace = True

    def build(self):
        return self.close_application_request


class LoadableInstrumentsRequest:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = act_ui_win_pb2.LoadableInstrumentsRequest(base=base)
        else:
            self._request = act_ui_win_pb2.LoadableInstrumentsRequest()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def load_all_instruments(self):
        self._request.loadAllInstruments = True

    def load_selected_instruments(self, instruments: list):
        for instrument in instruments:
            self._request.instruments.append(instrument)

    def build(self):
        return self._request
