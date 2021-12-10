import logging

from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base
from test_cases.wrapper import ret_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "RIN-1188"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty_step_2 = "1000"
    qty_step_5 = "500"
    price = "10"
    order_type_step2 = "Limit"
    order_type_step5 = "Market"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    side_step5 = "Sell"
    # end region

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create Limit order step 2
    ret_wrappers.create_order(base_request, qty_step_2, client, lookup, order_type_step2, tif, False, False, price, None, False,
                              False, None)
    # end region

    # region Verify order step 3
    ret_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'Qty', '1000', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'OrdType', 'Limit', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'Limit Price', '10', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'TIF', 'Day', False)
    # end region

    # region Cancel order step 4
    ret_wrappers.cancelle_order(base_request)
    # end region

    # region Verify order step 4
    ret_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', False)
    # end region

    # region Create Market order step 5
    ret_wrappers.create_order(base_request, qty_step_5, client, lookup, order_type_step5, tif, False, False, price, None,
                              side_step5, False, None)
    # end region

    # region Verify step 6
    ret_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'Qty', '500', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'OrdType', 'Market', False)
    ret_wrappers.verify_order_value(base_request, case_id, 'TIF', 'Day', False)
    # end region

    # region Cancel step 7
    ret_wrappers.cancelle_order(base_request)
    # end region

    # region Verify step 7
    ret_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', False)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
