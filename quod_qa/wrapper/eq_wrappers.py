from datetime import datetime, timedelta
from th2_grpc_act_gui_quod.order_book_pb2 import TransferOrderDetails, \
    ExtractManualCrossValuesRequest, GroupModifyDetails, ReassignOrderDetails
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from demo import logger
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
import time
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import direct_order_request, reject_order_request, direct_child_care_сorrect, \
    direct_loc_request, direct_moc_request, direct_loc_request_correct
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualCrossDetails, ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, accept_order_request

connectivity = "fix-ss-310-columbia-standart"  # 'fix-bs-310-columbia' # gtwquod5 fix-ss-310-columbia-standart
rule_connectivity = "fix-bs-310-columbia"
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


def cancel_order_via_fix(case_id, session, cl_order_id, org_cl_order_id, client, side):
    try:
        fix_manager_qtwquod = FixManager(connectivity, case_id)
        rule_manager = RuleManager()
        rule = rule_manager.add_OCR(session)
        cancel_parms = {
            "ClOrdID": cl_order_id,
            "Account": client,
            "Side": side,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": org_cl_order_id,
        }
        fix_cancel = FixMessage(cancel_parms)
        fix_manager_qtwquod.Send_OrderCancelRequest_FixMessage(fix_cancel)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)


def create_order(base_request, qty, client, lookup, order_type, tif="Day", is_care=False, recipient=None,
                 price=None, washbook=None, account=False,
                 is_sell=False, disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE, expire_date=None
                 ):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    if is_care:
        order_ticket.set_care_order(recipient, True, disclose_flag)
    order_ticket.set_tif(tif)
    if is_sell:
        order_ticket.sell()
    if price is not None:
        order_ticket.set_limit(price)
    if expire_date is not None:
        order_ticket.set_expire_date(expire_date)
    if washbook is not None:
        order_ticket.set_washbook(washbook)
    if account is not None:
        order_ticket.set_account(account)
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(rule_connectivity,
                                                                             "XPAR_" + client, "XPAR", int(price))
        call(order_ticket_service.placeOrder, new_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)


def create_order_via_fix(case_id, handl_inst, side, client, ord_type, qty, tif, price=None):
    try:
        rule_manager = RuleManager()
        fix_manager_qtwquod5 = FixManager(connectivity, case_id)
        fix_params = {
            'Account': client,
            'HandlInst': handl_inst,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif,
            'OrdType': ord_type,
            'Price': price,
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'Currency': 'EUR',
        }
        if price == None:
            fix_params.pop('Price')
            price = 0
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(rule_connectivity,
                                                                             "XPAR_" + client, "XPAR", int(price))
        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        response = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
        fix_params['response'] = response
        return fix_params
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)


def amend_order_via_fix(case_id, fix_message, parametr_list):
    fix_manager = FixManager(connectivity, case_id)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR(connectivity)
        fix_modify_message = FixMessage(fix_message)
        fix_modify_message.change_parameters(parametr_list)
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)


def amend_order(request, client=None, qty=None, price=None):
    order_amend = OrderTicketDetails()
    if not qty is None:
        order_amend.set_quantity(qty)
    if not price is None:
        order_amend.set_limit(price)
    if not client is None:
        order_amend.set_client(client)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_amend)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR(connectivity)
        call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)


def manual_cross_orders(request, qty, price, list, last_mkt):
    manual_cross_details = ManualCrossDetails(request)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_price(price)
    manual_cross_details.set_selected_rows(list)
    manual_cross_details.set_last_mkt(last_mkt)
    try:
        call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def manual_cross_orders_error(request, qty, price, list, last_mkt):
    error_message = ExtractManualCrossValuesRequest.ManualCrossExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractManualCrossValuesRequest.ManualCrossExtractedType.ERROR_MESSAGE
    request1 = ExtractManualCrossValuesRequest()
    request1.extractionId = "ManualCrossErrorMessageExtractionID"
    request1.extractedValues.append(error_message)
    req = ExtractManualCrossValuesRequest()
    req.CopyFrom(request1)
    manual_cross_details = ManualCrossDetails(request)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_price(price)
    manual_cross_details.set_selected_rows(list)
    manual_cross_details.set_last_mkt(last_mkt)
    try:
        call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def switch_user(session_id, case_id):
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    Stubs.win_act.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)


def accept_order(lookup, qty, price):
    try:
        call(Stubs.win_act.acceptOrder, accept_order_request(lookup, qty, price))
    except Exception:
        logger.error("Error execution", exc_info=True)


def accept_modify(lookup, qty, price):
    try:
        call(Stubs.win_act.acceptModifyPlusChild, accept_order_request(lookup, qty, price))
    except Exception:
        logger.error("Error execution", exc_info=True)


def direct_loc_order(qty, route):
    try:
        call(Stubs.win_act_order_book.orderBookDirectLoc, direct_loc_request_correct("UnmatchedQty", qty, route))
    except Exception:
        logger.error("Error execution", exc_info=True)


def direct_moc_order(qty, route):
    try:
        call(Stubs.win_act_order_book.orderBookDirectMoc, direct_moc_request("UnmatchedQty", qty, route))
    except Exception:
        logger.error("Error execution", exc_info=True)


def direct_child_care_order(qty, route, recipient, count):
    try:
        call(Stubs.win_act_order_book.orderBookDirectChildCare,
             direct_child_care_сorrect('UnmatchedQty', qty, recipient, route, count))
    except Exception:
        logger.error("Error execution", exc_info=True)


def reject_order(lookup, qty, price):
    try:
        call(Stubs.win_act.rejectOrder, reject_order_request(lookup, qty, price))
    except Exception:
        logger.error("Error execution", exc_info=True)


def direct_order(lookup, qty, price, qty_percent):
    try:
        call(Stubs.win_act.Direct, direct_order_request(lookup, qty, price, qty_percent))
    except Exception:
        logger.error("Error execution", exc_info=True)


def cancel_order(request):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(request)
    cancel_order_details.set_cancel_children(True)
    try:
        call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def split_limit_order(request, order_id, qty, type):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    order_split_limit.set_order_type(type)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split_limit)
    amend_order_details.set_filter(["Order ID", order_id])
    try:
        call(Stubs.win_act_order_book.splitLimit, amend_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def transfer_order(request, user):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    transfer_order_details = TransferOrderDetails()
    transfer_order_details.set_default_params(request)
    transfer_order_details.set_transfer_order_user(user, True)
    try:
        call(Stubs.win_act_order_book.transferOrder, transfer_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def manual_execution(request, qty, price, execution_firm='ExecutingTrader', contra_firm="Contra Firm"):
    manual_executing_details = ManualExecutingDetails(request)
    executions_details = manual_executing_details.add_executions_details()
    executions_details.set_quantity(qty)
    executions_details.set_price(price)
    executions_details.set_executing_firm(execution_firm)
    executions_details.set_contra_firm(contra_firm)
    executions_details.set_settlement_date_offset(1)
    executions_details.set_last_capacity("Agency")
    try:
        call(Stubs.win_act_order_book.manualExecution, manual_executing_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def complete_order(request):
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.completeOrder, complete_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def un_complete_order(request):
    un_complete_order_details = ModifyOrderDetails()
    un_complete_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.unCompleteOrder, un_complete_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def get_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("orderID")
    order_id = ExtractionDetail("order_id", "Order ID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    try:
        result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    except Exception:
        logger.error("Error execution", exc_info=True)
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


def verify_value(request, case_id, column_name, expected_value, is_child):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id(column_name)
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    if is_child:
        result = call(Stubs.win_act_order_book.getChildOrdersDetails, order_details.request())
    else:
        result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values(column_name, expected_value, result[value.name])
    verifier.verify()



def notify_dfd(request):
    notify_dfd_request = ModifyOrderDetails()
    notify_dfd_request.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.notifyDFD, notify_dfd_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def group_modify(request, client, security_account=None, routes=None, free_notes=None):
    group_modify_details = GroupModifyDetails()
    group_modify_details.base.CopyFrom(request)
    group_modify_details.client = client
    if security_account is not None:
        group_modify_details.securityAccount = security_account
    if routes is not None:
        group_modify_details.routes = routes
    if free_notes is not None:
        group_modify_details.freeNotes = free_notes
    try:
        call(Stubs.win_act_order_book.groupModify, group_modify_details)
    except Exception:
        logger.error("Error execution", exc_info=True)


def reassign_order(request, recipient):
    reassign_order_details = ReassignOrderDetails()
    reassign_order_details.base.CopyFrom(request)
    reassign_order_details.desk = recipient
    try:
        call(Stubs.win_act_order_book.reassignOrder, reassign_order_details)
    except Exception:
        logger.error("Error execution", exc_info=True)


def approve_block(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.approveMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def book_order(request, client, agreed_price, net_gross_ind="Gross", give_up_broker=None, trade_date=None,
               settlement_type=None, settlement_currency=None, exchange_rate=None, exchange_rate_calc=None,
               settlement_date=None, toggle_recompute=False, comm_basis=None, comm_rate=None, fees_basis=None,
               fees_rate=None,  misc_arr:[]= None):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    ticket_details = modify_request.add_ticket_details()
    ticket_details.set_client(client)
    ticket_details.set_net_gross_ind(net_gross_ind)
    ticket_details.set_agreed_price(agreed_price)
    if trade_date is not None:
        ticket_details.set_trade_date(trade_date)
    if give_up_broker is not None:
        ticket_details.set_give_up_broker(give_up_broker)

    settlement_details = modify_request.add_settlement_details()
    if settlement_type is not None:
        settlement_details.set_settlement_type(settlement_type)
    if settlement_currency is not None:
        settlement_details.set_settlement_currency(settlement_currency)
    if exchange_rate is not None:
        settlement_details.set_exchange_rate(exchange_rate)
    if exchange_rate_calc is not None:
        settlement_details.set_exchange_rate_calc(exchange_rate_calc)
    if settlement_date is not None:
        settlement_details.toggle_settlement_date()
        settlement_details.set_settlement_date(settlement_date)
    if toggle_recompute is not False:
        settlement_details.toggle_recompute()

    if comm_basis and comm_rate is not None:
        commissions_details = modify_request.add_commissions_details()
        commissions_details.toggle_manual()
        commissions_details.add_commission(basis=comm_basis, rate=comm_rate)

    if fees_basis and fees_rate is not None:
        fees_details = modify_request.add_fees_details()
        fees_details.add_fees(basis=fees_basis, rate=fees_rate)

    if misc_arr is not None:
        misc_details = modify_request.add_misc_details()
        misc_details.set_bo_field_1(misc_arr[0])
        misc_details.set_bo_field_2(misc_arr[1])
        misc_details.set_bo_field_3(misc_arr[2])
        misc_details.set_bo_field_4(misc_arr[3])
        misc_details.set_bo_field_5(misc_arr[4])

    extraction_details = modify_request.add_extraction_details()
    extraction_details.set_extraction_id("BookExtractionId")
    extraction_details.extract_net_price("book.netPrice")
    extraction_details.extract_net_amount("book.netAmount")
    extraction_details.extract_total_comm("book.totalComm")
    extraction_details.extract_gross_amount("book.grossAmount")
    extraction_details.extract_total_fees("book.totalFees")
    extraction_details.extract_agreed_price("book.agreedPrice")
    try:
        response = call(middle_office_service.bookOrder, modify_request.build())
        return response
    except Exception:
        logger.error("Error execution", exc_info=True)

def unbook_order (request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.unBookOrder, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)

def allocate_order (request,arr_allocation_param:[]):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)

    allocations_details = modify_request.add_allocations_details()
    '''
    example of arr_allocation_param:
   param=[{"Security Account": "YM_client_SA1", "Alloc Qty": "200"},
           {"Security Account": "YM_client_SA2", "Alloc Qty": "200"}]
    '''
    for i in arr_allocation_param:
        allocations_details.add_allocation_param(i)

    extraction_details = modify_request.add_extraction_details()
    extraction_details.set_extraction_id("BookExtractionId")
    extraction_details.extract_net_price("book.netPrice")
    extraction_details.extract_net_amount("book.netAmount")
    extraction_details.extract_total_comm("book.totalComm")
    extraction_details.extract_gross_amount("book.grossAmount")
    extraction_details.extract_total_fees("book.totalFees")
    extraction_details.extract_agreed_price("book.agreedPrice")
    try:
        response = call(middle_office_service.allocateMiddleOfficeTicket, modify_request.build())
        return response
    except Exception:
        logger.error("Error execution", exc_info=True)

def unallocate_order (request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.unAllocateMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)