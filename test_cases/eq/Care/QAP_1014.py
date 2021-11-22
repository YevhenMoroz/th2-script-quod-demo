import logging
from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers
from test_cases.wrapper.eq_fix_wrappers import create_order_via_fix
from stubs import Stubs
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1014"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)

    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)
    # endregion
    # region Accept CO
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Check values in OrderBook after Accept
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
