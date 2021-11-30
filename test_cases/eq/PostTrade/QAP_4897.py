import logging

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4897"
    # region Declarations
    qty = "500"
    price = "2"
    price2 = "3"
    client = "MOClient"
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
    fix_message1 = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    response1 = fix_message1.pop("response")
    fix_message2 = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price2)
    eq_wrappers.accept_order('VETO', qty, price)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price2)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price2)
    response2 = fix_message2.pop("response")
    eq_wrappers.cancel_execution(base_request, {"Qty": "250", "ExecPrice": price, "Client ID": client})
    eq_wrappers.cancel_execution(base_request, {"Qty": "250", "ExecPrice": price2, "Client ID": client})
    eq_wrappers.complete_order(base_request, 2)

    eq_wrappers.mass_book(base_request, [1, 2])
    eq_wrappers.verify_block_value(base_request, case_id, "Qty", "250",
                                   ["Order ID", response1.response_messages_list[0].fields['OrderID'].simple_value])
    eq_wrappers.verify_block_value(base_request, case_id, "Qty", "250",
                                   ["Order ID", response2.response_messages_list[0].fields['OrderID'].simple_value])
