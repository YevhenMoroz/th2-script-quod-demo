import logging

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4901"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "100"
    price = "10"
    client = "CLIENT_VSKULINEC"
    # Add this row, where we will be have norm version and realise client=CLIENT4
    lookup = "VETO"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create order via fix
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    # eq_wrappers.accept_order(lookup, qty, price) Add this row, where we will be have norm version and realise
    eq_wrappers.manual_execution(base_request, str(int(qty)/2), price)
    eq_wrappers.verify_order_value(base_request, case_id, 'DayCumAmt', 500)
    eq_wrappers.verify_order_value(base_request, case_id, 'DayAvgPrice', 10)