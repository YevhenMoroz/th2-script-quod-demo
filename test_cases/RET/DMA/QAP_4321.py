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
from test_framework.old_wrappers.ret_wrappers import extract_parent_order_details, verifier, amend_negative_ex, get_order_id, \
    extract_error_message_order_ticket, decorator_try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order(base_request, lookup, client, price, order_type, qty, tif, side):

    order_ticket_service = Stubs.win_act_order_ticket
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    if order_type == "Limit":
        order_ticket.set_order_type("Limit")
    if order_type == "Market":
        order_ticket.set_order_type("Market")
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    if side == 'Buy':
        order_ticket.buy()
    else:
        order_ticket.sell()
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP-4321"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations
    price = "20"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Create order Pre-condition
    create_order(base_request, lookup, client, price, order_type="Limit", qty="1300", tif="Day", side="Buy")
    # end region

    # region Create order step 1,2,3
    create_order(base_request, lookup, client, price, order_type="Market", qty="1300", tif="FillorKill", side="Sell")
    # end region

    # region Extract and Verify order status
    order_status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check order Status", expected_value="Filled", actual_value=order_status)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
