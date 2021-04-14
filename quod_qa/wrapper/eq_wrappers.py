from custom.basic_custom_actions import create_event
from demo import logger
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import set_base, accept_order_request
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

def open_fe(session_id, report_id, case_id, folder, user, password):
    init_event = create_event("Initialization", parent_id=report_id)
    set_base(session_id, case_id)
    if not Stubs.frontend_is_open:
        prepare_fe(init_event, session_id, folder, user, password)
    else:
        get_opened_fe(case_id, session_id)


def open_fe2(session_id, report_id,  folder, user, password):
    init_event = create_event("Initialization", parent_id=report_id)
    prepare_fe(init_event, session_id, folder, user, password)


def create_DMA(base_request, qty, client, lookup, order_type,tif="Day", price=None,sell_side=False):
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_client(client)
        order_ticket.set_order_type(order_type)
        order_ticket.set_tif(tif)
        if sell_side:
            order_ticket.sell()
        if price is not None:
            order_ticket.set_limit(price)
        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)

        order_ticket_service = Stubs.win_act_order_ticket
        call(order_ticket_service.placeOrder, new_order_details.build())

def create_Care(base_request, qty, client, lookup, order_type,resipient,tif="Day",to_user=False,price=None,sell_side=False):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_care_order(resipient,to_user)
    order_ticket.set_tif(tif)
    if sell_side:
        order_ticket.sell()
    if price is not None:
        order_ticket.set_limit(price)
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())
def switch_user(session_id, case_id):
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    Stubs.win_act.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)

def accept_order(lookup, qty, price):
    call(Stubs.win_act.acceptOrder, accept_order_request(lookup, qty, price))

def amend_order(values,base_request):
        order_amend = OrderTicketDetails()
        if 'new_price' in values:
            order_amend.set_limit(values['new_price'])
        if 'new_qty' in values:
            order_amend.set_quantity(values['new_qty'])
        if 'order_type' in values:
            order_amend.set_order_type(values['order_type'])
        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_order_details(order_amend)
        call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())
def cancelled_order(base_request):
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_id = ExtractionDetail("order_id", "Order ID")
    common_act = Stubs.win_act
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_id
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("Qty", order_qty.name, '50'),
                                                  verify_ent("LmtPrice", order_price.name,'2' )]))
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", ])
    call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())

def manual_execution(request, qty, price):
    manual_executing_details = ManualExecutingDetails(request)
    executions_details = manual_executing_details.add_executions_details()
    executions_details.set_quantity(qty)
    executions_details.set_price(price)
    executions_details.set_executing_firm("ExecutingFirm")
    executions_details.set_contra_firm("Contra_Firm")
    executions_details.set_last_capacity("Agency")
    call(Stubs.win_act_order_book.manualExecution, manual_executing_details.build())

def complete_order(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(request)
    call(Stubs.win_act_order_book.completeOrders, complete_order_details.build())