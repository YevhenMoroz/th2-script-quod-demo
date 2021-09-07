import logging
import os

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from quod_qa.wrapper.ret_wrappers import verifier, extract_parent_order_details, get_order_id, \
    extract_child_lvl1_order_details

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order(base_request, client, order_type, price, tif, lookup, qty, side, display_qty=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    if display_qty:
        order_ticket.set_display_qty(display_qty)
    if side == 'Buy':
        order_ticket.buy()
    elif side == 'Sell':
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket

    call(order_ticket_service.placeOrder, new_order_details.build())


def execute(session_id, report_id):
    case_name = "QAP_5175"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    client = "HAKKIM"
    order_type = "Limit"
    price = "1"
    tif = "Day"
    lookup = "T55FD"
    # endregion
    extraction_id = "ID"
    common_act = Stubs.win_act
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # end region

    # region create Iceberg algo order step 1
    create_order(base_request, client, order_type, price, tif, lookup, qty="1000", side='Sell', display_qty='500')
    # end region

    parent_order_id = get_order_id(base_request)

    # region Extract and Verify parent order details
    order_status = extract_parent_order_details(base_request, column_name='Sts', extraction_id=extraction_id)
    verifier(case_id, event_name='Check parent order Status', expected_value='Open', actual_value=order_status)

    order_display_qty = extract_parent_order_details(base_request, column_name='DisplQty', extraction_id=extraction_id)

    verifier(case_id, event_name='Check parent order Display Qty', expected_value='500', actual_value=order_display_qty)
    # end region

    # region Extract and Verify child Iceberg order details step 2
    child_order_id = extract_child_lvl1_order_details(base_request, column_name="Order ID",
                                                      extraction_id="Child Iceberg")
    child_order_sts = extract_child_lvl1_order_details(base_request, column_name="Sts", extraction_id=extraction_id)
    verifier(case_id, event_name="Check child order Status", expected_value="Open", actual_value=child_order_sts)

    child_order_display_qty = extract_child_lvl1_order_details(base_request, column_name="DisplQty",
                                                               extraction_id="Child Iceberg")
    verifier(case_id, event_name="Check child order Status", expected_value="DisplQty",
             actual_value=child_order_display_qty)
    child_order_execpcy = extract_child_lvl1_order_details(base_request, column_name="ExecPcy",
                                                           extraction_id=extraction_id)
    verifier(case_id, event_name="Check child order Execution Policy", expected_value="ExecPcy",
             actual_value=child_order_execpcy)
    # end region

    # region Create DMA order step 3
    create_order(base_request, client, order_type, price, tif, lookup, qty="500", side='Buy')
    # end region

    # region Extract and Verify child order details step 4
    order_status_new = extract_child_lvl1_order_details(base_request, column_name="Sts", extraction_id=extraction_id,
                                                        child_order_id=child_order_id)
    verifier(case_id, event_name="Check new child order Status", expected_value="Filled", actual_value=order_status_new)

    order_display_qty_new = extract_child_lvl1_order_details(base_request, column_name="CumQty",
                                                             extraction_id=extraction_id)
    verifier(case_id, event_name="Check new child order CumQty", expected_value="500",
             actual_value=order_display_qty_new)
    # end region
