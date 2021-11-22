import logging

from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_fix_wrappers
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4648"
    # region Declarations
    client = "CLIENT_YMOROZ"
    account = "CLIENT_YMOROZ_SA1"
    account2 = "CLIENT_YMOROZ_SA2"
    qty = "1800"
    price = "10"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)

    no_order=[eq_fix_wrappers.set_fix_order_detail("3", "2", client, 2, qty, 0, price),
              eq_fix_wrappers.set_fix_order_detail("3", "2", client, 2, qty, 0, price)]

    print(no_order)