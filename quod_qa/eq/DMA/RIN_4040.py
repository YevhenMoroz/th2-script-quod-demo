import logging

from datetime import datetime


from win_gui_modules.application_wrappers import LoginDetailsRequest, OpenApplicationRequest
from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.utils import set_session_id, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "RIN_4040"

    seconds, nanos = timestamps()  # Store case start time

    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    if not Stubs.frontend_is_open:

        stub = Stubs.win_act
        init_event = create_event("Initialization", parent_id=case_id)

        # region open FE login window
        open_app_req = OpenApplicationRequest()
        open_app_req.set_session_id(session_id)
        open_app_req.set_parent_event_id(init_event)
        open_app_req.set_work_dir(Stubs.custom_config['qf_trading_fe_folder'])
        open_app_req.set_application_file(Stubs.custom_config['qf_trading_fe_exec'])
        stub.openApplication(open_app_req.build())
        # end region

        # region input login details
        login_details_req = LoginDetailsRequest()
        login_details_req.set_session_id(session_id)
        login_details_req.set_parent_event_id(init_event)
        login_details_req.set_username("HD123")
        login_details_req.set_password("HD123")
        login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
        login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name'])
        login_details_req.is_error_expected(True)
        login_details_req.set_extraction_id("LoginErrorMessageExtraction")
        call(stub.login, login_details_req.build())
        # added method to close login window using Close button click
        login_details_req.close_login_windows()
        call(stub.login, login_details_req.build())
        # end region
    else:
        get_opened_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
