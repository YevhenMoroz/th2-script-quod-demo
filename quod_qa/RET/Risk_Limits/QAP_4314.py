import os

import logging

from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

from quod_qa.wrapper.eq_wrappers import create_order, verify_order_value

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "1.2"
    qty = "10000000"
    tif = "Day"
    client = "HAKKIM"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FE according to 1st and 2nd steps
    create_order(base_request, qty, client, lookup, order_type, tif,
                 False, None, price, None, None, False, False, None, False)
    # endregion

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Open", False)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
