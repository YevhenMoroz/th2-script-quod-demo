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

from test_framework.old_wrappers.ret_wrappers import create_order, verify_order_value, try_except

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
    order_type = "Limit"
    price = ["1234567,89", "100"]
    qty = ["100", "1234567891011", "200"]
    tif = "Day"
    client = "HAKKIM"
    symbol = "RELIANCE"
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FE according to 1st step
    create_order(base_request, qty[0], client, lookup, order_type, tif,
                 False, None, price[0], None, False, None, None)
    # endregion

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Open", False)
    # endregion

    # region Create order via FE according to 2nd step
    create_order(base_request, qty[1], client, lookup, order_type, tif,
                 False, None, price[1], None, False, None, None)
    # endregion

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Open", False)
    # endregion

    # region Create order via FE according to 3rd step
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty[2])
    order_ticket.set_limit(price[1])
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

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
