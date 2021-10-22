import logging
import os

from datetime import datetime
from custom.basic_custom_actions import timestamps
from custom.verifier import Verifier
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from custom import basic_custom_actions as bca
from quod_qa.wrapper.ret_wrappers import verifier, extract_error_message_order_ticket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order_iceberg(base_request, qty, client, order_type, price, tif, side, display_qty, lookup):

    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(lookup)
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    order_ticket.set_display_qty(display_qty)
    if side == 'Buy':
        order_ticket.buy()
    else:
        order_ticket.sell()
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.setOrderDetails, new_order_details.build())


def execute(session_id, report_id):
    case_name = "QAP_5122"

    seconds, nanos = timestamps()  # Store case start time
    order_ticket_service = Stubs.win_act_order_ticket
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations
    qty = "1,000"
    client = "HAKKIM"
    price = "10"
    order_type = "Limit"
    tif = "Day"
    side = "Buy"
    display_qty = "1300"
    lookup = "T55FD"
    expected_result = "Error - [QUOD-11605] 'DisplayQty' (1300) greater than 'OrdQty' (1000)"
    # end region

    # region create Iceberg order via FE step 1
    create_order_iceberg(base_request, qty, client, order_type, price, tif, side, display_qty, lookup)
    # end region

    # region Extract error message
    error_message = extract_error_message_order_ticket(base_request, order_ticket_service)
    verifier(case_id=case_id, event_name='Check error message', expected_value=expected_result,
             actual_value=error_message)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
