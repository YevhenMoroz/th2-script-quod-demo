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
from win_gui_modules.order_book_wrappers import ModifyOrderDetails

from test_cases.wrapper.ret_wrappers import get_order_id, verifier, extract_parent_order_details, \
    check_order_algo_parameters_book, cancel_order

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order_multilisting(base_request, order_ticket_service, qty, client, order_type, stop_price, tif, side,
                              lookup, allow_missing_prim=None, available_venue=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_stop_price(stop_price)
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


def amend_order(request, order_id=None, order_type=None, qty=None, stop_price=None, client=None, account=None):
    order_amend = OrderTicketDetails()
    if order_type is not None:
        order_amend.set_order_type(order_type)
    if qty is not None:
        order_amend.set_quantity(qty)
    if stop_price is not None:
        order_amend.set_stop_price(stop_price)
    if client is not None:
        order_amend.set_client(client)
    if account is not None:
        order_amend.set_account(account)
    amend_order_details = ModifyOrderDetails()
    if order_id is not None:
        amend_order_details.set_filter(["Order ID", order_id])
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_amend)
    call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())


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
    stop_price = ["20", "19", "21"]
    qty = ["1300", "1,000", "1,500"]
    tif = "Day"
    client = "test_api_client"
    side = "Sell"
    # endregion

    # region Create order via FE according to 1st - 4th steps
    create_order_multilisting(base_request, order_ticket_service, qty[0], client, order_type, stop_price[0], tif, side,
                              lookup, allow_missing_prim=True, available_venue=True)
    # endregion

    order_id = get_order_id(base_request)

    # region Check values in Order book according to 4th step
    algo_parameters = check_order_algo_parameters_book(base_request, order_id, order_book_service)

    verifier(case_id, event_name="Check AllowMissingPrimary Status", expected_value="True",
             actual_value=algo_parameters["ParametersValue row_0"])
    verifier(case_id, event_name="Check AvailableVenues Status", expected_value="True",
             actual_value=algo_parameters["ParametersValue row_1"])

    order_status = extract_parent_order_details(base_request=base_request, column_name="Sts",
                                                extraction_id="Extract Order Status", order_id=order_id)
    ord_type = extract_parent_order_details(base_request=base_request, column_name="OrdType",
                                            extraction_id="Extract Order Type", order_id=order_id)

    verifier(case_id=case_id, event_name="Verify Order Status", expected_value="Open", actual_value=order_status)
    verifier(case_id=case_id, event_name="Verify Order Type", expected_value="Stop", actual_value=ord_type)
    # endregion

    # region Modify order via FE according to 5st step
    amend_order(base_request, order_id, order_type, qty[1], stop_price[1], client=None, account=None)
    # endregion

    # region Check values in Order book according to 5th step
    order_status = extract_parent_order_details(base_request=base_request, column_name="Qty",
                                                extraction_id="Extract Order Quantity", order_id=order_id)
    order_stop_price = extract_parent_order_details(base_request=base_request, column_name="Stop Price",
                                                    extraction_id="Extract Order Stop Price", order_id=order_id)

    verifier(case_id=case_id, event_name="Verify Order Quantity", expected_value=qty[1],
             actual_value=order_status)
    verifier(case_id=case_id, event_name="Verify Order Stop Price", expected_value=stop_price[1],
             actual_value=order_stop_price)
    # endregion

    # region Modify order via FE according to 6st step
    amend_order(base_request, order_id, order_type, qty[2], stop_price[2], client=None, account=None)
    # endregion

    # region Check values in Order book according to 6th step
    order_status = extract_parent_order_details(base_request=base_request, column_name="Qty",
                                                extraction_id="Extract Order Quantity", order_id=order_id)
    order_stop_price = extract_parent_order_details(base_request=base_request, column_name="Stop Price",
                                                    extraction_id="Extract Order Stop Price", order_id=order_id)

    verifier(case_id=case_id, event_name="Verify Order Quantity", expected_value=qty[2],
             actual_value=order_status)
    verifier(case_id=case_id, event_name="Verify Order Stop Price", expected_value=stop_price[2],
             actual_value=order_stop_price)
    # endregion

    # region Cancel order via FE according to 7st step
    cancel_order(base_request, order_id, is_child=False)
    # endregion

    # region Check values in Order book according to 7th step
    order_status = extract_parent_order_details(base_request=base_request, column_name="Sts",
                                                extraction_id="Extract Order Status", order_id=order_id)

    verifier(case_id=case_id, event_name="Verify Order Status", expected_value="Cancelled", actual_value=order_status)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
