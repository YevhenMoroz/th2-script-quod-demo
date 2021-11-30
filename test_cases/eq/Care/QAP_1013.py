import logging
from datetime import datetime

from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, call
from win_gui_modules.wrappers import verification, verify_ent, reject_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1013"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    order_type = "Limit"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    desk = Stubs.custom_config['qf_trading_fe_user_desk']
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username, price=price)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)
    # endregion
    # region Reject CO
    call(common_act.rejectOrder, reject_order_request(lookup, qty, price))
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Rejected")
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
