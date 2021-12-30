import logging
import os

from custom import basic_custom_actions as bca
from datetime import datetime

from test_framework.old_wrappers.ret_wrappers import close_order_book, decorator_try_except
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent
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
    case_name = "QAP_4323"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "3000"
    price = "50"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create order via FE according with step 1
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, False, price, False, False,
                             None)

    extraction_id = "order.dma"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)

    call(order_book_service.getOrdersDetails, order_details.request())
    # end region

    # region Check values in OrderBook(expected result for step 1)
    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(extraction_id, "Checking order status after created",
                                                 [verify_ent("Status", order_status.name, "Open")]))
    # end region

    # region Cancel order according with step 3
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_comment("Order cancelled by script")

    call(order_book_service.cancelOrder, cancel_order_details.build())
    # end region

    # region Check values after Cancel (expected result for step 3)
    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(extraction_id, "Checking order status after cancelled",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled")]))
    # end region

    # region Amend order according with step 4
    amend_negative_ex(base_request, order_book_service)
    # endregion

    close_order_book(base_request, Stubs.win_act_order_book)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
