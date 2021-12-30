import logging
from datetime import datetime

from th2_grpc_hand import rhbatch_pb2

from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe, switch_user
from win_gui_modules.utils import get_base_request, close_fe

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id,session_id):
    case_name = "QAP-1019"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    order_type = "Limit"

    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    init_event = create_event("Initialization", parent_id=report_id)
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    eq_wrappers.open_fe2(session_id2, report_id, work_dir, username2, password2)
    # endregion
    # region switch user 1
    switch_user()
    # endregion1
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username2,
                             price=price,recipient_user=True)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    # endregion
    # region switch to user2
    switch_user()
    # endregion
    # region Reject CO
    eq_wrappers.reject_order(lookup, qty, price)
    # endregion
    # region switch to user1
    switch_user()
    # endregion
    # region Check values in OrderBook after Accept
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Rejected")
    # endregion

    close_fe(case_id, session_id2)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
