import os

import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from custom.basic_custom_actions import timestamps

from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from test_framework.old_wrappers.ret_wrappers import create_order, direct_loc_order_via_inbox, verify_order_value, get_order_id, \
    force_cancel_order

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "100"
    qty = "300"
    tif = "Day"
    client = "HAKKIM"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FE
    create_order(base_request, qty, client, lookup, order_type, tif,
                 True, recipient, price, None, False, DiscloseFlagEnum.DEFAULT_VALUE, None)
    # endregion

    # region Create LOC child MO
    direct_loc_order_via_inbox("50", "NSE")
    # endregion

    # region Check values of child MO in OrderBook (Child Orders) according to 1st step
    verify_order_value(base_request, case_id, "Sts", "Open", True)
    # endregion

    # region Cancel order via FE according to 2nd step
    order_id = get_order_id(base_request)
    force_cancel_order(base_request, order_id, True)
    # endregion

    # region Check values of child MO in OrderBook (Child Orders) according to 2nd step
    verify_order_value(base_request, case_id, "Sts", "Cancelled", True)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
