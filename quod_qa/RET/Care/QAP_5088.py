import os

import logging

from datetime import datetime

from th2_grpc_hand import rhbatch_pb2

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.utils import get_base_request, set_session_id, prepare_fe, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from quod_qa.wrapper.ret_wrappers import switch_user, create_order, verify_order_value, amend_order, get_order_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "100"
    qty = ["499", "500"]
    tif = "Day"
    client = "HAKKIM"
    recipient = "QA3"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    init_event = create_event("Initialization", parent_id=report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    prepare_fe(init_event, session_id2, work_dir, username2, password2)
    # endregion

    # region Switch to User 1
    switch_user(session_id, case_id)
    # endregion

    # region Create order via FE according to 1st step by User 1
    create_order(base_request, qty[0], client, lookup, order_type, tif,
                 True, recipient, price, None, False, DiscloseFlagEnum.DEFAULT_VALUE, None)
    # endregion

    # region Check values in OrderBook according to 2nd step by User 1
    verify_order_value(base_request, case_id, "Sts", "Open", False)
    verify_order_value(base_request, case_id, "Qty", "499", False)
    # endregion

    # region Switch to User 2
    switch_user(session_id2, case_id)
    # endregion

    # region Amend order via FE according to 3rd step by User 2
    order_id = get_order_id(base_request2)
    amend_order(request=base_request2, order_id=order_id, qty=qty[1])
    # endregion

    # region Check values in OrderBook according to 3rd step by User 2
    verify_order_value(base_request2, case_id, "Sts", "Open", False)
    verify_order_value(base_request2, case_id, "Qty", "500", False)
    # endregion

    # region Switch to User 1
    switch_user(session_id, case_id)
    # endregion

    # region Check values in OrderBook according to 3rd step by User 1
    verify_order_value(base_request, case_id, "Sts", "Open", False)
    verify_order_value(base_request, case_id, "Qty", "500", False)
    # endregion

    close_fe(case_id, session_id2)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
