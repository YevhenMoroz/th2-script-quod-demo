import logging

from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call
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


def create_order_extracting_error(base_request, qty, client, lookup, tif, order_type=None, price=None, sell_side=False):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_instrument(lookup)
    order_ticket.set_tif(tif)
    if order_type:
        order_ticket.set_order_type(order_type)
        order_ticket.set_limit(price)
    if sell_side:
        order_ticket.sell()
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.setOrderDetails, new_order_details.build())


def verifier(case_id, event_name, filed_name, expected_result, actual_result):
    verifier_step1 = Verifier(case_id)
    verifier_step1.set_event_name(event_name)
    verifier_step1.compare_values(filed_name, expected_result, actual_result)
    verifier_step1.verify()


def execute(session_id, report_id):
    case_name = "QAP_4209"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    client = "HAKKIM"
    lookup = "T55FD"
    order_type = "Limit"
    tif = "Day"
    price = "10"
    expected_rezult = 'Quantity cannot be negative or null'
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create order according with step 1
    create_order_extracting_error(base_request, "0", client, lookup, tif, order_type, price)
    # end region

    result_qty_zero = extract_error_message_order_ticket(base_request, order_ticket_service)

    # expected result for step 1
    verifier(case_id, "Check error message step 1", "Login Error with qty - 0", expected_rezult,
             result_qty_zero["ErrorMessage"])
    # end region

    # region Create order according with step 2
    eq_wrappers.create_order(base_request, "1.5", client, lookup, order_type, tif, False, None, price, False, False,
                             None)
    # end region

    # expected result for step 2
    eq_wrappers.verify_value(base_request, case_id, "Qty", "15", False)
    # end region

    # region Create order according with step 3
    create_order_extracting_error(base_request, "a%/", client, lookup, tif, order_type, price)
    # end region

    # expected result for step 3
    result_qty_symbols = extract_error_message_order_ticket(base_request, order_ticket_service)

    verifier(case_id, "Check error message step 2", "Login Error with qty - a%/", expected_rezult,
             result_qty_symbols["ErrorMessage"])
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
