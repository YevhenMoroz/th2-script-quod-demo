import logging
import os

from custom import basic_custom_actions as bca
from datetime import datetime
from custom.verifier import Verifier
from test_framework.old_wrappers.ret_wrappers import decorator_try_except
from win_gui_modules.application_wrappers import LoginDetailsRequest, OpenApplicationRequest
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def verifier_for_login_fe(case_id, step_number, expected_value, response):
    # region verifier
    verifier = Verifier(case_id)
    verifier.set_event_name(f"Check error for step {step_number}")
    verifier.compare_values("Login Error", expected_value, response["LoginError"][0:44])
    verifier.verify()
    # end region


def login_fe(stub, session_id, init_event, case_id, username, password, expected_value, step_number):
    # region open FE login window for step 1
    open_app_req = OpenApplicationRequest()
    open_app_req.set_session_id(session_id)
    open_app_req.set_parent_event_id(init_event)
    open_app_req.set_work_dir(Stubs.custom_config['qf_trading_fe_folder'])
    open_app_req.set_application_file(Stubs.custom_config['qf_trading_fe_exec'])
    stub.openApplication(open_app_req.build())
    # end region for step 1

    # region input login details step 1
    login_details_req = LoginDetailsRequest()
    login_details_id = "LoginErrorMessageExtraction"
    login_details_req.set_session_id(session_id)
    login_details_req.set_parent_event_id(init_event)
    login_details_req.set_username(username)
    login_details_req.set_password(password)
    login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
    login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name'])
    login_details_req.is_error_expected(True)
    login_details_req.set_extraction_id(login_details_id)
    login_details_req.close_login_windows()
    response = call(stub.login, login_details_req.build())
    # end region

    # region verifier
    verifier_for_login_fe(case_id, step_number, expected_value, response)
    # end region


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "RIN_4278"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    expected_value = "code=QUOD-17512:User credentials are invalid"

    if not Stubs.frontend_is_open:

        stub = Stubs.win_act
        init_event = create_event("Initialization", parent_id=case_id)

        # region login according with step 1
        login_fe(stub, session_id, init_event, case_id, " ", "H_pasSD3", expected_value, "1")
        # end region login for step 1

        # region login according with step 2
        login_fe(stub, session_id, init_event, case_id, "HD3", " ", expected_value, "2")
        # end region login for step 2

        # region login according with step 3
        login_fe(stub, session_id, init_event, case_id, "HD123", "HD123", expected_value, "3")
        # end region for step 3

        # region login according with step 4
        login_fe(stub, session_id, init_event, case_id, " ", " ", expected_value, "4")
        # end region for step 4

    else:
        get_opened_fe(case_id, session_id)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
