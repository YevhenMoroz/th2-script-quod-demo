import os

import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from custom.basic_custom_actions import timestamps

from stubs import Stubs

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

from test_framework.old_wrappers.ret_wrappers import get_order_id, verifier, extract_parent_order_details, \
    check_order_algo_parameters_book

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order_multilisting(base_request, order_ticket_service, qty, client, order_type, tif, side, lookup,
                              allow_missing_prim=None, available_venue=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    if side == "Buy":
        order_ticket.buy()
    elif side == "Sell":
        order_ticket.sell()
    multilisting_strategy = order_ticket.add_multilisting_strategy("Quod MultiListing")
    multilisting_strategy.set_allow_missing_prim(allow_missing_prim)
    multilisting_strategy.set_available_venues(available_venue)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())


def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    lookup = "SBIN"
    order_type = "Market"
    qty = "1300"
    tif = "AtTheClose"
    client = "HAKKIM"
    side = "Sell"
    # endregion

    # region Create order via FE according to 1st - 4th steps
    create_order_multilisting(base_request, order_ticket_service, qty, client, order_type, tif, side, lookup,
                              allow_missing_prim=True, available_venue=True)
    # endregion

    order_id = get_order_id(base_request)

    # region Check values in Order book according to 5th step
    algo_parameters = check_order_algo_parameters_book(base_request, order_id, order_book_service)

    verifier(case_id, event_name="Check AllowMissingPrimary Status", expected_value="True",
             actual_value=algo_parameters["ParametersValue row_0"])
    verifier(case_id, event_name="Check AvailableVenues Status", expected_value="True",
             actual_value=algo_parameters["ParametersValue row_1"])

    order_status = extract_parent_order_details(base_request=base_request, column_name="Sts",
                                                extraction_id="Extract Order Status", order_id=order_id)

    verifier(case_id=case_id, event_name="Verify Order Status", expected_value="Eliminated", actual_value=order_status)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
