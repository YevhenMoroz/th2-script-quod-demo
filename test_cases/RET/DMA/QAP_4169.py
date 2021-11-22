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
from test_cases.wrapper.ret_wrappers import extract_parent_order_details, verifier

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


def execute(session_id, report_id):
    case_name = "QAP-4169"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations

    qty = "1300"
    price = "20"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "TCS"
    side = 'Sell'
    pos_validity = "Delivery"
    # end region
    # region Create order step 2
    create_order(base_request, qty, client, order_type, price, tif, side, pos_validity, lookup)
    # end region

    # region Extract and Verify order details step 3
    status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check Status", expected_value="Open", actual_value=status)

    pos_validity = extract_parent_order_details(base_request, column_name="PosValidity", extraction_id="PosVal")
    verifier(case_id, event_name="Check Position Validity", expected_value="Delivery", actual_value=pos_validity)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")