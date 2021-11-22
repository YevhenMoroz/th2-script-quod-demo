import logging

import quod_qa.wrapper.eq_fix_wrappers
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1365"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion

    eq_wrappers.split_limit_order(base_request, qty, 'Limit', '21')
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View", result['ErrorMessage'],
                            "Error - [QUOD-11605] 'Price' (21) greater than Parent's 'Price' (20)"
                            )
    verifier.verify()

