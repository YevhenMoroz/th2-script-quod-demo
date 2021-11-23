import logging
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4896"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "1.12345678"
    client = "MOClient"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    response = fix_message.pop('response')
    order = response.response_messages_list[0].fields['OrderID'].simple_value
    fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    response = fix_message.pop('response')
    order2 = eq_wrappers.get_order_value(base_request,"Order ID")
    # endregion
    # region Execute CO
    eq_wrappers.manual_execution(base_request, qty, price)
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region Mass Book
    eq_wrappers.mass_book(base_request, [1, 2])
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "AvgPx", price[:7], ['Order ID', order])
    eq_wrappers.verify_block_value(base_request, case_id, "AvgPx", price[:7], ['Order ID', order2])
    # endregion
