import logging

from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails

from win_gui_modules.application_wrappers import LoginDetailsRequest
from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo

from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, direct_loc_request
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "RIN_4040"

    seconds, nanos = timestamps()  # Store case start time

    # region Open FE

    login_details_req = LoginDetailsRequest()
    stub = Stubs.win_act
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    login_details_req.set_session_id(session_id)
    login_details_req.set_parent_event_id(case_id)
    login_details_req.set_username("dbdbdbfd")
    login_details_req.set_password("cwcrecrecgr")
    login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
    login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name'])
    login_details_req.is_error_expected(True)
    login_details_req.set_extraction_id("LoginErrorMessageExtraction")
    call(stub.login, login_details_req.build())

