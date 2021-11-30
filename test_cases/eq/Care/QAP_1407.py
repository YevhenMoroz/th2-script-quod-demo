import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1407"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    order_type = "Limit"

    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create CO
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    # region Verify
    result=eq_wrappers.is_menu_item_present(base_request,"Group Modify")
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Menu Item")
    verifier.compare_values("FeeAgent", "false", result['isMenuItemPresent'])
    verifier.verify()
    # endregion
