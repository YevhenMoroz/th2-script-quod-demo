import logging

from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from quod_qa.wrapper import ret_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "RIN-1188"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty_precondiiton = "5000"
    price_precondition = "50"
    side_precondition = "Sell"
    qty = "1000"
    price = "10"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    #
    # # region Pre-condition
    ret_wrappers.create_order(base_request, qty_precondiiton, client, lookup, order_type, tif, False, False,
                              price_precondition, None, side_precondition, False, None)
    # end region

    # region Create Limit order step 2
    ret_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, False, price, None, False,
                              False, None)
    # end region

    # region Verify order step 3
    ret_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'Qty', '1000', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'OrdType', 'Limit', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'Limit Price', '10', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'TIF', 'Day', False)
    # end region

    # region Amend qty step 4
    ret_wrappers.amend_order(base_request, qty="1500")
    # end region

    # region Amend price step 5
    ret_wrappers.amend_order(base_request, price="50")
    # # end region
    #
    # # region Amend order type step 6
    ret_wrappers.amend_order(base_request, order_type="Market")
    # end region

