import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4617"
    # region Declarations
    qty = "800"
    client = "CLIENT_FIX_CARE"
    price = "40"
    price2 = '200'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    # endregion
    # region Create order via FIX
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    response = fix_message.pop('response')
    # endregion
    # region Check values in OrderBook
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    eq_wrappers.manual_execution(base_request, str(int(int(qty) / 2)), price)
    eq_wrappers.complete_order(base_request)
    eq_wrappers.split_order(base_request, str(int(int(qty) / 2)), 'Limit', price)
    response = eq_wrappers.extract_error_order_ticket(base_request)
    print(response)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Error', "Error - [QUOD-24812] Invalid 'DoneForDay': " + order_id,
                            response['ErrorMessage'])
    verifier.verify()
