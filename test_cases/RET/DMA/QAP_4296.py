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


def create_order(base_request, lookup, price, client, order_type, qty, tif, side, account=None, wash_book_account=None):

    order_ticket_service = Stubs.win_act_order_ticket
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    order_ticket.set_client(client)
    if account:
        order_ticket.set_account(account)
    if order_type == "Limit":
        order_ticket.set_order_type("Limit")
    if order_type == "Market":
        order_ticket.set_order_type("Market")
    if wash_book_account:
        order_ticket.set_washbook(wash_book_account)
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
    case_name = "QAP-4296"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations
    price = "20"
    lookup = "T55FD"
    # end region

    # region Create order step 1,2
    create_order(base_request, lookup, price, client="POOJA", order_type="Limit", qty="1300",
                 tif="Day", side="Buy", account="HAKKIM3")
    # end region

    # region Extract and Verify step 3
    order_status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check order Status", expected_value="Open", actual_value=order_status)

    order_account = extract_parent_order_details(base_request, column_name="Account ID", extraction_id="Account")
    verifier(case_id, event_name="Check order Account ID", expected_value="HAKKIM3", actual_value=order_account)
    # end region

    # region Create order step 4,5,6
    create_order(base_request, lookup, price, client="HAKKIM", order_type="Limit", qty="1300",
                 tif="Day", side="Buy", wash_book_account="CareWB")
    # end region

    # region Extract and Verify step 6
    new_order_status = extract_parent_order_details(base_request, column_name="Sts", extraction_id="Sts")
    verifier(case_id, event_name="Check order Status", expected_value="Open", actual_value=new_order_status)

    order_washbook = extract_parent_order_details(base_request, column_name="Wash Book", extraction_id="Account")
    verifier(case_id, event_name="Check order Account ID", expected_value="CareWB", actual_value=order_washbook)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")


