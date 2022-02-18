import os

import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from custom.basic_custom_actions import timestamps

from stubs import Stubs

from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from test_framework.old_wrappers.ret_wrappers import create_order, verify_order_value, check_order_benchmark_book, get_order_id, \
    try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "111"
    qty = "222"
    tif = "Day"
    client = "HAKKIM"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    # endregion

    # region Create order via FE
    create_order(base_request, qty, client, lookup, order_type, tif,
                 True, recipient, price, None, False, DiscloseFlagEnum.DEFAULT_VALUE, None)
    # endregion

    # region Check values in OrderBook
    verify_order_value(base_request, case_id, "Sts", "Sent", False)
    # endregion

    # region Check values in Benchmark tab according to 1st step
    order_id = get_order_id(base_request)
    check_order_benchmark_book(base_request, case_id, ob_act, order_id, "Status", "New")
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
