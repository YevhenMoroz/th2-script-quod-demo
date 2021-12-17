import logging
import os

from custom import basic_custom_actions as bca
from datetime import datetime

from test_framework.old_wrappers.ret_wrappers import decorator_try_except
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from test_framework.old_wrappers import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def amend_negative_ex(base_request, order_book_service):
    # region Amend order
    order_amend = OrderTicketDetails()
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_order_details(order_amend)
    amend_order_details.set_default_params(base_request)
    amend_order_details.amend_by_icon()
    call(order_book_service.amendOrder, amend_order_details.build())
    # endregion


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4309"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book
    qty = "50"
    price = "100"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create buy order according with step 1
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, False, price, False, False,
                             None)

    # region Check values in OrderBook(expected result for step 1)
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Open", False)
    # end region

    # region Create sell order according with step 2
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, None, price, True, False, None)
    # end region

    # region Check values in OrderBook(expected result for step 2)
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Terminated", False)
    eq_wrappers.verify_value(base_request, case_id, "ExecSts", "Filled", False)
    eq_wrappers.verify_value(base_request, case_id, "ExecType", "DoneForDay", False)
    # end region

    # region check full filled order can't cancel according with step 3
    amend_negative_ex(base_request, order_book_service)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")