import os

import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from custom.basic_custom_actions import timestamps

from stubs import Stubs

from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

from test_framework.old_wrappers.ret_wrappers import verify_order_value, try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def extract_error_message_order_ticket(base_request, order_ticket_service):
    # extract rates tile table values
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
    return result


@try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket

    lookup = "RELIANCE"
    # "0-111111111" using to bypass the inability to enter a minus after clearing a "Price" field
    price = ["0", "0-111111111", "10", "abc"]
    stop_price = ["20", "abc"]
    qty = "400"
    client = "HAKKIM"
    symbol = "RELIANCE"
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FE according to 1st step
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[0])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Rejected", False)
    verify_order_value(base_request, case_id, "FreeNotes", "11603 'Price' (0) negative or zero", False)
    # endregion

    # region Create order via FE according to 2nd step
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[1])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Rejected", False)
    verify_order_value(base_request, case_id, "FreeNotes", "11603 'Price' (-99999999) negative or zero", False)
    # endregion

    # region Create order via FE according to 3rd step
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[2])
    order_ticket.set_stop_price(stop_price[0])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Rejected", False)
    verify_order_value(base_request, case_id, "FreeNotes", "11605 'StopPrice' (20) greater than 'Price' (10)", False)
    # endregion

    # region Create order via FE according to 4th step
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[3])
    order_ticket.set_stop_price(stop_price[1])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Rejected", False)
    verify_order_value(base_request, case_id, "FreeNotes", "11603 'Price' (0) negative or zero", False)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
