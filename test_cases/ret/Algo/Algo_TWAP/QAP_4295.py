import logging
import os

from datetime import datetime

from test_framework.old_wrappers.ret_wrappers import decorator_try_except
from win_gui_modules.order_book_wrappers import OrdersDetails, CancelOrderDetails

from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent
from test_framework.old_wrappers import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4295"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "1,000"
    price = "1"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create Algo(TWAP) order via FE according with step 1
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    order_ticket.set_limit(price)
    order_ticket.buy()

    twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
    twap_strategy.set_start_date("Now")
    twap_strategy.set_end_date("Now", "0.5")
    twap_strategy.set_waves("4")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())
    # end region

    order_id = eq_wrappers.get_order_id(base_request)

    # region extract and verify Parent details(expected result for step 1)
    extraction_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    order_details.set_filter(["Order ID", order_id])

    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    # parent request
    call(order_book_service.getOrdersDetails, order_details.request())

    call(common_act.verifyEntities, verification(extraction_id, "Checking order status",
                                                 [verify_ent("Order Status", order_status.name, "Open")]))
    # end region extraction and verify

    # region Cancel order according with step 2
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", order_id])
    cancel_order_details.set_comment("Order cancelled by script")

    call(order_book_service.cancelOrder, cancel_order_details.build())
    # end region

    # region Check values after Cancel(expected result in step 2)
    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(extraction_id, "Checking order status after cancelled",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled")]))
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")