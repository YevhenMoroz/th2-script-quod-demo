from datetime import datetime
from urllib import request

from th2_grpc_act_gui_quod.order_book_pb2 import TransferOrderDetails, NotifyDfdDetails, ExtractManualCrossValuesRequest
from copy import deepcopy
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from demo import logger
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
import time
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import set_base, accept_order_request, direct_order_request, reject_order_request, \
    direct_moc_request, direct_loc_request, direct_child_care
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualCrossDetails, ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request, direct_child_care_сorrect

connectivity = "fix-bs-310-columbia" #'fix-ss-310-columbia-standart' # gtwquod5 fix-ss-310-columbia-standart
order_book_act = Stubs.win_act_order_book
common_act = Stubs.win_act


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


def cancel_order_via_fix(request, order_id, case_id, client_order_id, client, side):
    fix_manager_qtwquod = FixManager(connectivity, case_id)
    order_id = request[order_id.name]
    client_order_id = request[client_order_id.name]
    cancel_parms = {
        "ClOrdID": order_id,
        "Account": client,
        "Side": side,
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": client_order_id,
    }
    fix_cancel = FixMessage(cancel_parms)
    fix_manager_qtwquod.Send_OrderCancelRequest_FixMessage(fix_cancel)


def create_order(base_request, qty, client, lookup, order_type, tif="Day", is_care=False, recipient=None,
                 price=None,
                 sell_side=False, disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE, expire_date=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    if is_care:
        order_ticket.set_care_order(recipient, False, disclose_flag)
    order_ticket.set_tif(tif)
    if sell_side:
        order_ticket.sell()
    if price is not None:
        order_ticket.set_limit(price)
    if expire_date is not None:
        order_ticket.set_expire_date(expire_date)
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())


def create_order_via_fix(case_id, HandlInst, side, client, ord_type, qty, tif, price=None):
    try:
        rule_manager = RuleManager()
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
            'Price': price,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'Currency': 'EUR',
        }
        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        response = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
        fix_params['response'] = response
        return fix_params
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)


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


def amend_order_via_fix(fix_message, case_id, parametr_list):
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR("fix-bs-eq-paris")
        fix_modify_message = FixMessage(fix_message)
        fix_manager_qtwquod = FixManager(connectivity, case_id)
        fix_modify_message.change_parameters(parametr_list)
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager_qtwquod.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)
    return fix_modify_message.get_parameter('Price')


def manual_cross_orders(request, qty, price, list, last_mkt):
    manual_cross_details = ManualCrossDetails(request)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_price(price)
    manual_cross_details.set_selected_rows(list)
    manual_cross_details.set_last_mkt(last_mkt)
    call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())


def manual_cross_orders_error(request, qty, price, list, last_mkt):
    error_message = ExtractManualCrossValuesRequest.ManualCrossExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractManualCrossValuesRequest.ManualCrossExtractedType.ERROR_MESSAGE
    request1 = ExtractManualCrossValuesRequest()
    request1.extractionId = "ManualCrossErrorMessageExtractionID"
    request1.extractedValues.append(error_message)
    manual_cross_details = ManualCrossDetails(request)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_price(price)
    manual_cross_details.set_selected_rows(list)
    manual_cross_details.set_last_mkt(last_mkt)
    manual_cross_details.manualCrossValues.CopyFrom(request1)
    response = call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())
    return response


def switch_user(session_id, case_id):
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    Stubs.win_act.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)


def accept_order(lookup, qty, price):
    call(Stubs.win_act.acceptOrder, accept_order_request(lookup, qty, price))


def accept_modify(lookup, qty, price):
    call(Stubs.win_act.acceptModifyPlusChild, accept_order_request(lookup, qty, price))


def direct_loc_order(qty, route):
    call(Stubs.win_act_order_book.orderBookDirectLoc, direct_loc_request("UnmatchedQty", qty, route))


def direct_moc_order(qty, route):
    call(Stubs.win_act_order_book.orderBookDirectMoc, direct_moc_request("UnmatchedQty", qty, route))


def direct_child_care_order(qty, route, recipient, count):
    call(Stubs.win_act_order_book.orderBookDirectChildCare,
         direct_child_care_сorrect('UnmatchedQty', qty, recipient, route, count))


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


def cancelle_order(request):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(request)
    cancel_order_details.set_cancel_children(True)
    call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())


def split_limit_order(request, order_id, qty, type):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    # if not price in None:
    #    order_split_limit.set_limit(price)
    order_split_limit.set_order_type(type)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split_limit)
    amend_order_details.set_filter(["Order ID", order_id])
    call(Stubs.win_act_order_book.splitLimit, amend_order_details.build())


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
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(request)
    call(Stubs.win_act_order_book.completeOrder, complete_order_details.build())


def un_complete_order(request):
    un_complete_order_details = ModifyOrderDetails()
    un_complete_order_details.set_default_params(request)
    call(Stubs.win_act_order_book.unCompleteOrder, un_complete_order_details.build())


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


def verify_value(request, case_id, column_name, expected_value):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id(column_name)
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values(column_name, expected_value, result[value.name])
    verifier.verify()


def check_time_sleep_fix_order(request, fix_message, time1):
    for i in range(1, 4):
        if(get_cl_order_id(request) == fix_message['ClOrdID']):
            time.sleep(time1)
        else:
            break

def notify_dfd(request):
    notify_dfd_request = ModifyOrderDetails()
    notify_dfd_request.set_default_params(request)
    call(Stubs.win_act_order_book.notifyDFD, notify_dfd_request.build())
