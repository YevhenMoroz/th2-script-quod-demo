import logging
from datetime import datetime

from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute(report_id, session_id):
    case_name = "QAP-4971"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "100"
    price = "10"
    client = "CLIENT_YMOROZ"
    lookup = 'VETO'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create DMA order
    eq_wrappers.create_order(base_request, qty, client, lookup, '2', 'Day', False, price=price, is_button=True,
                             instrument='VETO')
    #  endregion
    # region    Extract error
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View",
                            "Error - [QUOD-11656] User 'vskulinec' cannot use account group 'CLIENT_YMOROZ'",
                            result['ErrorMessage']
                            )
    verifier.verify()
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
