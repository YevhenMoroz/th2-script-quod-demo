import logging
from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1012"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    order_type = "Limit"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    desk = Stubs.custom_config['qf_trading_fe_user_desk']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=desk, price=price)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)
    # endregion
    # region Accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Check values in OrderBook after Accept
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
