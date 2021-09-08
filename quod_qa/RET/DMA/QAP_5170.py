import logging
import os

from datetime import datetime

from custom.basic_custom_actions import timestamps
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from quod_qa.wrapper.ret_wrappers import extract_parent_order_details, verifier, amend_negative_ex, get_order_id,\
    extract_error_message_order_ticket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order(base_request, qty, client, order_type, price, tif, side, pos_validity, lookup):

    order_ticket_service = Stubs.win_act_order_ticket
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    order_ticket.set_general_tab_in_advanced(pos_validity)
    if side == 'Buy':
        order_ticket.buy()
    else:
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())


def amend_order(base_request, pos_validity, order_id):
    order_amend = OrderTicketDetails()
    order_amend.set_general_tab_in_advanced(pos_validity)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)
    amend_order_details.set_filter(["Order ID", order_id])
    call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())


def execute(session_id, report_id):
    case_name = "QAP-5170"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations

    qty_1 = "1300"
    qty_2 = "1000"
    price = "20"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    side_buy = "Buy"
    side_sell = 'Sell'
    pos_validity = "Delivery"
    error_message = "Error - [QUOD-24819] Modification of 'PosValidity' from DEL to TP1 is not allowed for 'OrdModify'"
    # end region

    # region Create order step 2, 3
    create_order(base_request, qty_1, client, order_type, price, tif, side_sell, pos_validity, lookup)
    # end region

    first_order_id = get_order_id(base_request)

    # region Extract and Verify order details step 3
    status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check Status", expected_value="Open", actual_value=status)

    pos_validity = extract_parent_order_details(base_request, column_name="PosValidity", extraction_id="PosVal")
    verifier(case_id, event_name="Check Position Validity", expected_value="Delivery", actual_value=pos_validity)
    # end region

    # region Create opposite order step 4
    create_order(base_request, qty_2, client, order_type, price, tif, side_buy, pos_validity, lookup)
    # end region

    # region Extract adn Verify opposite order step 4
    status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check Status", expected_value="Terminated", actual_value=status)

    pos_validity = extract_parent_order_details(base_request, column_name="PosValidity", extraction_id="PosVal")
    verifier(case_id, event_name="Check Position Validity", expected_value="Delivery", actual_value=pos_validity)
    # end region

    amend_negative_ex(base_request, order_book_service=Stubs.win_act_order_book)

    # region Amend order step 5
    amend_order(base_request, pos_validity="BTST", order_id=first_order_id)
    # end region

    extracted_error_message = extract_error_message_order_ticket(base_request, Stubs.win_act_order_ticket)
    verifier(case_id, event_name="Check Error Message", expected_value=error_message,
             actual_value=extracted_error_message["ErrorMessage"][0:97])
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")