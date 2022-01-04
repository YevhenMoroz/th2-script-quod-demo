import logging
import os
from custom import basic_custom_actions as bca
from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from test_framework.old_wrappers.ret_wrappers import decorator_try_except
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from test_cases.wrapper import ret_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4313"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
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
    ret_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, True, recipient, price, None, False,
                              DiscloseFlagEnum.DEFAULT_VALUE)
    # end region

    # region Check values in OrderBook according step 6
    ret_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent", False)

    # endregion

    # region accept order according with step 7,8
    ret_wrappers.accept_order(lookup, qty, price)
    # end region

    # region Check value in child order according with step 10
    ret_wrappers.verify_order_value(base_request, case_id, "Sts", "Open", False)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
