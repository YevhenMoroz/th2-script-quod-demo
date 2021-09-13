import logging
import os
from custom import basic_custom_actions as bca
from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, direct_order_request
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "QAP_4286"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book
    qty = "100"
    client = "HAKKIM"
    lookup = "T55FD"
    order_type = "Limit"
    tif = "Day"
    price = "30"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create Care order via FE according with step 1,2,3,4,5
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, True, recipient, price, False,
                             DiscloseFlagEnum.DEFAULT_VALUE)
    # end region

    # region Check values in OrderBook according step 6
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Sent", False)

    # endregion

    # region accept order according with step 7,8
    eq_wrappers.accept_order(lookup, qty, price)
    # end region

    # region direct order according with step 9
    call(order_book_service.orderBookDirectOrder, direct_order_request(lookup, qty, price, "100"))
    # end region

    # region Check value in child order according with step 10
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Open", True)
    eq_wrappers.verify_value(base_request, case_id, "Qty", qty, True)

    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
