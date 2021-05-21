import logging

from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "RIN_1143"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act

    qty = "50"
    price = "10"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "TCS"
    # end region

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # end region

    # region Create buy order
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())

    order_id = eq_wrappers.get_order_id(base_request)
    # end region

    # region Create sell order

    sell_order_ticket = OrderTicketDetails()
    sell_order_ticket.set_quantity(qty)
    sell_order_ticket.set_limit(price)
    sell_order_ticket.set_order_type(order_type)
    sell_order_ticket.set_tif(tif)
    sell_order_ticket.set_client(client)
    sell_order_ticket.sell()

    new_sell_order_details = NewOrderDetails()
    new_sell_order_details.set_lookup_instr(lookup)
    new_sell_order_details.set_order_details(sell_order_ticket)
    new_sell_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_sell_order_details.build())
    # end region

    # region filter
    extraction_id = "order.dma"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    order_details.set_filter(["Order ID", order_id])

    call(order_book_service.getOrdersDetails, order_details.request())
    # end region

    # region Check values in OrderBook
    order_status = ExtractionDetail("order_status", "Sts")
    order_exec = ExtractionDetail("order_exec", "ExecSts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_exec])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Status", order_status.name, "Terminated"),
                                                      verify_ent("ExecSts", order_exec.name, "Filled")]))

    # end region

    # region Cancel order
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", order_id])

    # The system shouldn't find Cancel function, this is negative case
    call(order_book_service.cancelOrder, cancel_order_details.build())
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")






