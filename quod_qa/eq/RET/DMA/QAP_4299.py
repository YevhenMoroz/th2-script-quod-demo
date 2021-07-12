import logging

from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def extract_error_message_order_ticket(base_request, order_ticket_service):
    # extract rates tile table values
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
    return result


def execute(report_id):
    case_name = "QAP_4299"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "5,000,000"
    client = "HAKKIM"
    lookup = "TCS"
    order_type = "Limit"
    tif = "Day"
    price = "4.0"
    expected_value = "Error - [QUOD-11814] 'OrdQty' (1.1e+07) greater than 'MaxOrdQty' (1e+07)"
    # endregion

    # region Open FE
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # end region

    # region Create order according with step 1 and step 2
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, None, price, False, False, None)
    # end region

    # region Check values in OrderBook(expected result in step 2)
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Open", False)
    eq_wrappers.verify_value(base_request, case_id, "Qty", qty, False)
    eq_wrappers.verify_value(base_request, case_id, "LmtPrice", "4", False)
    # end region check value

    # region Amend order according with step 3
    order_amend = OrderTicketDetails()
    order_amend.set_quantity("11,000,000")
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)

    call(order_book_service.amendOrder, amend_order_details.build())
    # end region

    # region Extract error in order ticket
    result_amend_qty = extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region extract

    # region verify details(expected result in step 3)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check error message in order ticket")
    verifier.compare_values("Amend error message", expected_value, result_amend_qty["ErrorMessage"])
    verifier.verify()
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")