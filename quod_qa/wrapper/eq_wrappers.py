from datetime import datetime, timedelta

from th2_grpc_act_gui_quod import middle_office_service, order_book_service
from th2_grpc_act_gui_quod.order_book_pb2 import TransferOrderDetails, \
    ExtractManualCrossValuesRequest, GroupModifyDetails, ReassignOrderDetails
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from demo import logger
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ViewOrderExtractionDetails, \
    ExtractMiddleOfficeBlotterValuesRequest, AllocationsExtractionDetails
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import direct_order_request, reject_order_request, direct_child_care_сorrect, \
    direct_loc_request, direct_moc_request, direct_loc_request_correct
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualCrossDetails, ManualExecutingDetails, BaseOrdersDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, accept_order_request

buy_connectivity = "fix-buy-317ganymede-standard"  # 'fix-bs-310-columbia' # fix-ss-back-office fix-buy-317ganymede-standard
sell_connectivity = "fix-sell-317ganymede-standard"  # fix-sell-317ganymede-standard # gtwquod5 fix-ss-310-columbia-standart
bo_connectivity = "fix-sell-317-backoffice"
order_book_act = Stubs.win_act_order_book
common_act = Stubs.win_act


def get_buy_connectivity():
    return buy_connectivity


def get_sell_connectivity():
    return sell_connectivity


def get_bo_connectivity():
    return bo_connectivity


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
        fix_manager_qtwquod = FixManager(buy_connectivity, case_id)
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
                 price=None, washbook=None, account=None,
                 is_sell=False, disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE, expire_date=None, recipient_user=False
                 ):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    if is_care:
        order_ticket.set_care_order(recipient, recipient_user, disclose_flag)
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(sell_connectivity,
                                                                             client + "_PARIS", "XPAR", int(price))
        call(order_ticket_service.placeOrder, new_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)

'''
  instrument ={
                'Symbol': 'IS0000000001_EUR',
                'SecurityID': 'IS0000000001',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XEUR'
            }
'''
def create_order_via_fix(case_id, handl_inst, side, client, ord_type, qty, tif, price=None, no_allocs=None,
                         insrument=None):
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris",
                                                                             "XPAR_" + client, "XPAR", int(price))
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
            'NoAllocs': no_allocs,
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'Currency': 'EUR',
        }
        fix_params.update()
        if price == None:
            fix_params.pop('Price')
        if no_allocs == None:
            fix_params.pop('NoAllocs')
        if insrument != None:
            fix_params.update(Instrument=insrument)
        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        response = fix_manager.Send_NewOrderSingle_FixMessage(fix_message)
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

def amend_order_via_fix(case_id, fix_message, parametr_list):
    fix_manager = FixManager(buy_connectivity, case_id)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR(buy_connectivity)
        fix_modify_message = FixMessage(fix_message)
        fix_modify_message.change_parameters(parametr_list)
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)


def amend_order(request, client=None, qty=None, price=None, account=None):
    order_amend = OrderTicketDetails()
    if not qty is None:
        order_amend.set_quantity(qty)
    if not price is None:
        order_amend.set_limit(price)
    if not client is None:
        order_amend.set_client(client)
    if not account is None:
        order_amend.set_account(account)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_amend)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR(buy_connectivity)
        call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())
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


def split_limit_order(request, qty, type, price):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    order_split_limit.set_order_type(type)
    order_split_limit.set_limit(price)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split_limit)

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


def get_is_locked(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("IsLocked")
    is_locked = ExtractionDetail("IsLocked", "IsLocked")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[is_locked])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    try:
        result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    except Exception:
        logger.error("Error execution", exc_info=True)
    return result[is_locked.name]


def get_cl_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("ClOrdID")
    cl_order_id = ExtractionDetail("cl_order_id", "ClOrdID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[cl_order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[cl_order_id.name]


def verify_order_value(request, case_id, column_name, expected_value, is_child=False):
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


def verify_block_value(request, case_id, column_name, expected_value):
    ext_id = "MiddleOfficeExtractionId"
    middle_office_service = Stubs.win_act_middle_office_service
    extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=request)
    extract_request.set_extraction_id(ext_id)
    extraction_detail = ExtractionDetail(column_name, column_name)
    extract_request.add_extraction_details([extraction_detail])
    request = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking block order")
    verifier.compare_values(column_name, expected_value, request[extraction_detail.name])
    verifier.verify()


def verify_allocate_value(request, case_id, column_name, expected_value, account=None):
    extract_request = AllocationsExtractionDetails(base=request)
    middle_office_service = Stubs.win_act_middle_office_service
    if account is not None:
        extract_request.set_allocations_filter({"Account ID": account})
    extraction_detail = ExtractionDetail(column_name, column_name)
    order_details = extract_request.add_order_details()
    order_details.add_extraction_details([extraction_detail])
    request_allocate_blotter = call(middle_office_service.extractAllocationsTableData, extract_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking allocate blotter")
    verifier.compare_values(column_name, expected_value, request_allocate_blotter[extraction_detail.name])
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


def check_booking_toggle_manual(base_request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=base_request)
    modify_request.add_commissions_details()
    extraction_details = modify_request.add_extraction_details()
    extraction_details.set_extraction_id("BookExtractionId")
    extraction_details.extract_manual_checkbox_state("book.manualCheckboxState")
    return call(middle_office_service.bookOrder, modify_request.build())


def book_order(request, client, agreed_price, net_gross_ind="Gross", give_up_broker=None, trade_date=None,
               settlement_type=None, settlement_currency=None, exchange_rate=None, exchange_rate_calc=None,
               settlement_date=None, pset=None, toggle_recompute=False, comm_basis=None, comm_rate=None,
               fees_basis=None,
               fees_rate=None, fees_type=None, fees_category=None, misc_arr: [] = None, remove_commission=False,
               remove_fees=False):
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
    if pset is not None:
        settlement_details.set_pset(pset)
    if toggle_recompute is not False:
        settlement_details.toggle_recompute()

    commissions_details = modify_request.add_commissions_details()
    if comm_basis is not None:
        # response = check_booking_toggle_manual(request)
        # if response['book.manualCheckboxState'] == 'unchecked':
        commissions_details.toggle_manual()
        commissions_details.add_commission(comm_basis, comm_rate)
    if remove_commission:
        commissions_details.remove_commissions()
    fees_details = modify_request.add_fees_details()
    if fees_basis is not None:
        fees_details.add_fees(fees_type, fees_basis, rate=fees_rate, category=fees_category)
    if remove_fees:
        fees_details.remove_fees()

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
    extraction_details.extract_pset_bic("book.psetBic")
    extraction_details.extract_exchange_rate("book.settlementType")
    extraction_details.extract_settlement_type("book.exchangeRate")
    try:
        response = call(middle_office_service.bookOrder, modify_request.build())
        return response
    except Exception:
        logger.error("Error execution", exc_info=True)


def amend_block(request, agreed_price=None, net_gross_ind=None, give_up_broker=None, trade_date=None,
                settlement_type=None,
                settlement_currency=None, exchange_rate=None, exchange_rate_calc=None, settlement_date=None, pset=None,
                comm_basis=None, comm_rate=None, fees_basis=None, fees_rate=None, fee_type=None, fee_category=None,
                misc_arr: [] = None, remove_commissions=False, remove_fees=False):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)

    ticket_details = modify_request.add_ticket_details()
    if net_gross_ind is not None:
        ticket_details.set_net_gross_ind(net_gross_ind)
    if agreed_price is not None:
        ticket_details.set_agreed_price(agreed_price)
    if trade_date is not None:
        ticket_details.set_trade_date(trade_date)
    if give_up_broker is not None:
        ticket_details.set_give_up_broker(give_up_broker)
    if net_gross_ind is not None:
        ticket_details.set_net_gross_ind(net_gross_ind)
    if agreed_price is not None:
        ticket_details.set_agreed_price(agreed_price)

    settlement_details = modify_request.add_settlement_details()
    if settlement_type is not None:
        settlement_details.set_settlement_currency(settlement_type)
    if settlement_currency is not None:
        settlement_details.set_settlement_currency(settlement_currency)
    if exchange_rate is not None:
        settlement_details.set_exchange_rate(exchange_rate)
    if exchange_rate_calc is not None:
        settlement_details.set_exchange_rate_calc(exchange_rate_calc)
    if settlement_date is not None:
        settlement_details.toggle_settlement_date()
        settlement_details.set_settlement_date(settlement_date)
    if pset is not None:
        settlement_details.set_pset(pset)

    if remove_commissions:
        commissions_details = modify_request.add_commissions_details()
        commissions_details.remove_commissions()
    if remove_fees:
        fees_details = modify_request.add_fees_details()
        fees_details.remove_fees()
    if comm_basis and comm_rate is not None:
        commissions_details = modify_request.add_commissions_details()
        response = check_booking_toggle_manual(request)
        if response['book.manualCheckboxState'] != 'checked':
            commissions_details.toggle_manual()
        commissions_details.add_commission(comm_basis, comm_rate)
    if fees_basis and fees_rate is not None:
        fees_details = modify_request.add_fees_details()
        fees_details.add_fees(fee_type, fees_basis, fees_rate, category=fee_category)

    if misc_arr is not None:
        misc_details = modify_request.add_misc_details()
        misc_details.set_bo_field_1(misc_arr[0])
        misc_details.set_bo_field_2(misc_arr[1])
        misc_details.set_bo_field_3(misc_arr[2])
        misc_details.set_bo_field_4(misc_arr[3])
        misc_details.set_bo_field_5(misc_arr[4])

    extraction_details = modify_request.add_extraction_details()
    extraction_details.set_extraction_id("BookExtractionId", )
    extraction_details.extract_net_price("book.netPrice")
    extraction_details.extract_net_amount("book.netAmount")
    extraction_details.extract_total_comm("book.totalComm")
    extraction_details.extract_gross_amount("book.grossAmount")
    extraction_details.extract_total_fees("book.totalFees")
    extraction_details.extract_agreed_price("book.agreedPrice")
    extraction_details.extract_pset_bic("book.psetBic")
    extraction_details.extract_exchange_rate("book.settlementType")
    extraction_details.extract_settlement_type("book.exchangeRate")

    try:
        return call(middle_office_service.amendMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def unbook_order(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.unBookOrder, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def allocate_order(request, arr_allocation_param: []):
    modify_request = ModifyTicketDetails(base=request)

    allocations_details = modify_request.add_allocations_details()
    '''
    example of arr_allocation_param:
   param=[{"Security Account": "YM_client_SA1", "Alloc Qty": "200"},
           {"Security Account": "YM_client_SA2", "Alloc Qty": "200"}]
    '''
    for i in arr_allocation_param:
        allocations_details.add_allocation_param(i)
    '''
    extraction_details = modify_request.add_extraction_details()
    extraction_details.extract_agreed_price("book.agreedPrice")
    extraction_details.extract_gross_amount("book.grossAmount")
    extraction_details.extract_total_comm("book.totalComm")
    extraction_details.extract_total_fees("book.totalFees")
    extraction_details.extract_net_price("book.netPrice")
    extraction_details.extract_net_amount("book.netAmount")
    extraction_details.extract_pset_bic("book.psetBic")
    extraction_details.extract_exchange_rate("book.exchangeRate")
    '''
    try:
        response = call(Stubs.win_act_middle_office_service.allocateMiddleOfficeTicket, modify_request.build())
        return response
    except Exception:
        logger.error("Error execution", exc_info=True)


def amend_allocate(request, account=None, agreed_price=None, settlement_currency=None, exchange_rate=None,
                   exchange_rate_calc=None,
                   settlement_date=None, pset=None, comm_basis=None, comm_rate=None, fees_basis=None, fees_rate=None,
                   fee_type=None, fee_category=None, misc_arr: [] = None, remove_commissions=False, remove_fees=False):
    modify_request = ModifyTicketDetails(base=request)
    amend_allocations_details = modify_request.add_amend_allocations_details()
    ticket_details = modify_request.add_ticket_details()
    if account is not None:
        amend_allocations_details.set_allocations_filter({"Account ID": account})
    if agreed_price is not None:
        ticket_details.set_agreed_price(agreed_price)
    settlement_details = modify_request.add_settlement_details()
    if settlement_currency is not None:
        settlement_details.set_settlement_currency(settlement_currency)
    if exchange_rate is not None:
        settlement_details.set_exchange_rate(exchange_rate)
    if exchange_rate_calc is not None:
        settlement_details.set_exchange_rate_calc(exchange_rate_calc)
    if settlement_date is not None:
        settlement_details.set_settlement_date(settlement_date)
    if pset is not None:
        settlement_details.set_pset(pset)

    if remove_commissions:
        commissions_details = modify_request.add_commissions_details()
        commissions_details.remove_commissions()
    if remove_fees:
        fees_details = modify_request.add_fees_details()
        fees_details.remove_fees()
    if comm_basis and comm_rate is not None:
        commissions_details = modify_request.add_commissions_details()
        commissions_details.toggle_manual()
        commissions_details.add_commission(comm_basis, comm_rate)
    if fees_basis and fees_rate is not None:
        fees_details = modify_request.add_fees_details()
        fees_details.add_fees(fee_type, fees_basis, fees_rate, category=fee_category)

    if misc_arr is not None:
        misc_details = modify_request.add_misc_details()
        misc_details.set_bo_field_1(misc_arr[0])
        misc_details.set_bo_field_2(misc_arr[1])
        misc_details.set_bo_field_3(misc_arr[2])
        misc_details.set_bo_field_4(misc_arr[3])
        misc_details.set_bo_field_5(misc_arr[4])
    '''
    extraction_details = modify_request.add_extraction_details()
    extraction_details.extract_agreed_price("book.agreedPrice")
    extraction_details.extract_gross_amount("book.grossAmount")
    extraction_details.extract_total_comm("book.totalComm")
    extraction_details.extract_total_fees("book.totalFees")
    extraction_details.extract_net_price("book.netPrice")
    extraction_details.extract_net_amount("book.netAmount")
    extraction_details.extract_pset_bic("book.psetBic")
    extraction_details.extract_exchange_rate("book.exchangeRate")
    '''
    try:
        return call(Stubs.win_act_middle_office_service.amendAllocations, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def unallocate_order(request):
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(Stubs.win_act_middle_office_service.unAllocateMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def check_in_order(request):
    order_book_obj = ModifyOrderDetails()
    order_book_obj.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.checkInOrder, order_book_obj.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def check_out_order(request):
    order_book_obj = ModifyOrderDetails()
    order_book_obj.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.checkOutOrder, order_book_obj.build())
    except Exception:
        logger.error("Error execution", exc_info=True)


def view_orders_for_block(request, count: int):
    middle_office_service = Stubs.win_act_middle_office_service
    extract_request = ViewOrderExtractionDetails(base=request)
    lenght = "middleOffice.viewOrdersCount"
    extract_request.extract_length(lenght)
    arr_response = []
    for i in range(1, count + 1):
        order_details = extract_request.add_order_details()
        order_details.set_order_number(i)
        dma_order_id_view = ExtractionDetail("middleOffice.orderId", "Order ID")
        order_details.add_extraction_detail(dma_order_id_view)
    try:
        arr_response.append(call(middle_office_service.extractViewOrdersTableData, extract_request.build()))
        return arr_response
    except Exception:
        logger.error("Error execution", exc_info=True)


def check_error_in_book(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(request)
    modify_request.set_partial_error_message("qwerty")
    try:
        error = call(middle_office_service.bookOrder, modify_request.build())
        return error
    except Exception:
        logger.error("Error execution", exc_info=True)


def re_order_leaves(request, is_sall=False):
    base_orders_details = BaseOrdersDetails(request)
    call(Stubs.win_act_order_book.reOrderLeaves, base_orders_details.build())
