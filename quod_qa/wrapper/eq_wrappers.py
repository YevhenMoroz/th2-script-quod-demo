from datetime import datetime
from th2_grpc_act_gui_quod.order_book_pb2 import TransferOrderDetails
from custom.basic_custom_actions import create_event
from demo import logger
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import direct_order_request, reject_order_request, \
    direct_moc_request, direct_loc_request
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, accept_order_request

connectivity = 'gtwquod5'


def open_fe(session_id, report_id, case_id, folder, user, password):
    init_event = create_event("Initialization", parent_id=report_id)
    set_base(session_id, case_id)
    if not Stubs.frontend_is_open:
        prepare_fe(init_event, session_id, folder, user, password)
    else:
        get_opened_fe(case_id, session_id)


def open_fe2(session_id, report_id, folder, user, password):
    init_event = create_event("Initialization", parent_id=report_id)
    prepare_fe(init_event, session_id, folder, user, password)


def cancel_order_via_fix(order_id, client_order_id, client, case_id, side):
    fix_manager_qtwquod = FixManager(connectivity, case_id)
    cancel_parms = {
        "ClOrdID": order_id,
        "Account": client,
        "Side": side,
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": client_order_id,
    }
    fix_cancel = FixMessage(cancel_parms)
    fix_manager_qtwquod.Send_OrderCancelRequest_FixMessage(fix_cancel)


def create_order(base_request, qty, client, lookup, order_type, tif="Day", is_care=False, recipient=None, price=None,
                 sell_side=False):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    if is_care:
        order_ticket.set_care_order(recipient)
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


def create_order_via_fix(case_id, HandlInst, side, client, ord_type, qty, tif, price=None):
    try:
        rule_manager = RuleManager()
        if price != None:
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris",
                                                                                 "XPAR_" + client, "XPAR", int(price))
        fix_manager_qtwquod5 = FixManager(connectivity, case_id)

        fix_params = {
            'Account': client,
            'HandlInst': HandlInst,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif,
            'OrdType': ord_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'Currency': 'EUR',
        }
        if price is not None:
            fix_modify_message = FixMessage(fix_params)
            fix_modify_message.change_parameter('Price', price)

        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
        return fix_params
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)


def amend_order_via_fix(fix_message, case_id, parametr_list):
    fix_manager_qtwquod = FixManager(connectivity, case_id)
    fix_modify_message = FixMessage(fix_message)
    fix_modify_message.change_parameters(parametr_list)
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_qtwquod.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)


def switch_user(session_id, case_id):
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    Stubs.win_act.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)


def accept_order(lookup, qty, price):
    call(Stubs.win_act.acceptOrder, accept_order_request(lookup, qty, price))


def direct_loc_order(qty, route):
    call(Stubs.win_act_order_book.orderBookDirectLoc, direct_loc_request("UnmatchedQty", qty, route))


def direct_moc_order(qty, route):
    call(Stubs.win_act_order_book.orderBookDirectMoc, direct_moc_request("UnmatchedQty", qty, route))


def reject_order(lookup, qty, price):
    call(Stubs.win_act.rejectOrder, reject_order_request(lookup, qty, price))


def direct_order(lookup, qty, price, qty_percent):
    call(Stubs.win_act.Direct, direct_order_request(lookup, qty, price, qty_percent))


def amend_order(request, qty=None, price=None):
    order_amend = OrderTicketDetails()
    if not qty in None:
        order_amend.set_quantity(qty)
    if not price in None:
        order_amend.set_limit(price)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_amend)
    call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())


def cancel_order(request):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(request)
    cancel_order_details.set_cancel_children(True)
    call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())


def split_limit_order(request, qty, type, price=None):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    if price is not None:
        order_split_limit.set_limit(price)
    order_split_limit.set_order_type(type)
    order_details = ModifyOrderDetails()
    order_details.set_default_params(request)
    order_details.set_order_details(order_split_limit)
    call(Stubs.win_act_order_book.splitLimit, order_details.build())


def split_order(request, qty, type, price=None):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    if price is not None:
        order_split_limit.set_limit(price)
    order_split_limit.set_order_type(type)
    order_details = ModifyOrderDetails()
    order_details.set_default_params(request)
    order_details.set_order_details(order_split_limit)
    call(Stubs.win_act_order_book.splitOrder, order_details.build())


def transfer_order(request, user):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    transfer_order_details = TransferOrderDetails()
    transfer_order_details.set_default_params(request)
    transfer_order_details.set_transfer_order_user(user, True)
    call(Stubs.win_act_order_book.transferOrder, transfer_order_details.build())


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


def get_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("orderID")
    order_id = ExtractionDetail("order_id", "Order ID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[order_id.name]


def get_cl_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("ClOrdID")
    cl_order_id = ExtractionDetail("cl_order_id", "ClOrdID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[cl_order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[cl_order_id.name]
