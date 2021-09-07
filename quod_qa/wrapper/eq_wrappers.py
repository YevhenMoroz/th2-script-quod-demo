from th2_grpc_act_gui_quod.basket_ticket_pb2 import ImportedFileMappingField
from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from th2_grpc_act_gui_quod.order_book_pb2 import ExtractManualCrossValuesRequest, GroupModifyDetails, \
    ReassignOrderDetails

from custom import basic_custom_actions
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier, VerificationMethod
from demo import logger
from quod_qa.wrapper.eq_fix_wrappers import buy_connectivity, sell_connectivity
from rule_management import RuleManager
from stubs import Stubs
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from custom import basic_custom_actions as bca
from win_gui_modules import trades_blotter_wrappers, basket_order_book_wrappers
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.basket_ticket_wrappers import ImportedFileMappingFieldDetails, ImportedFileMappingDetails, \
    TemplatesDetails, RowDetails, FileDetails, FileType, BasketTicketDetails
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ViewOrderExtractionDetails, \
    ExtractMiddleOfficeBlotterValuesRequest, AllocationsExtractionDetails
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.trades_blotter_wrappers import MatchDetails, ModifyTradesDetails
from win_gui_modules.utils import prepare_fe, get_opened_fe, call
from win_gui_modules.wrappers import direct_order_request, reject_order_request, direct_child_care_сorrect, \
    direct_loc_request_correct, direct_moc_request_correct
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualCrossDetails, ManualExecutingDetails, MenuItemDetails, TransferOrderDetails, BaseOrdersDetails, \
    SuspendOrderDetails, AddToBasketDetails, TransferPoolDetailsCLass, InternalTransferActionDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, accept_order_request


def scroll_order_book(request, count: int = 1):
    scrolling_details = GridScrollingDetails(ScrollingOperation.UP, count, request)
    call(Stubs.win_act_order_book.orderBookGridScrolling, scrolling_details.build())


def extract_error_order_ticket(base_request):
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
    return result


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


def create_order(base_request, qty, client, lookup, order_type, tif="Day", is_care=False, recipient=None,
                 price=None, washbook=None, account=None,
                 is_sell=False, disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE, expire_date=None, recipient_user=False,
                 capacity=None
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
    if capacity is not None:
        order_ticket.set_capacity(capacity)
    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    order_ticket_service = Stubs.win_act_order_ticket
    try:
        call(order_ticket_service.placeOrder, new_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail create_order', status="FAIL")


'''
  instrument ={
                'Symbol': 'IS0000000001_EUR',
                'SecurityID': 'IS0000000001',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XEUR'
            }
'''


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
        basic_custom_actions.create_event('Fail amend_order', status="FAIL")
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
        basic_custom_actions.create_event('Fail manual_cross_orders', status="FAIL")
        logger.error("Error execution", exc_info=True)


def manual_cross_orders_error(request, qty, price, list, last_mkt):
    error_message = ExtractManualCrossValuesRequest.ManualCrossExtractedValue()
    error_message.name = "Error"
    req = ExtractManualCrossValuesRequest()
    req.extractionId = 'ManualCrossErrorMessageExtractionID'
    req.extractedValues.append(error_message)
    manual_cross_details = ManualCrossDetails(request)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_price(price)
    manual_cross_details.set_selected_rows(list)
    manual_cross_details.set_last_mkt(last_mkt)
    manual_cross_details.manualCrossValues.CopyFrom(req)
    try:
        reply = call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())
        return reply
    except Exception:
        basic_custom_actions.create_event('Fail manual_cross_orders_error', status="FAIL")
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
        basic_custom_actions.create_event('Fail accept_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def accept_modify(lookup, qty, price):
    try:
        call(Stubs.win_act.acceptModifyPlusChild, accept_order_request(lookup, qty, price))
    except Exception:
        basic_custom_actions.create_event('Fail accept_modify', status="FAIL")
        logger.error("Error execution", exc_info=True)


def accept_cancel(lookup, qty, price):
    try:
        call(Stubs.win_act.acceptAndCancelChildren, accept_order_request(lookup, qty, price))
    except Exception:
        basic_custom_actions.create_event('Fail accept_cancel', status="FAIL")
        logger.error("Error execution", exc_info=True)


def direct_loc_order(qty, route):
    try:
        call(Stubs.win_act_order_book.orderBookDirectLoc, direct_loc_request_correct("UnmatchedQty", qty, route))
    except Exception:
        basic_custom_actions.create_event('Fail direct_loc_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def direct_moc_order(qty, route):
    try:
        call(Stubs.win_act_order_book.orderBookDirectMoc, direct_moc_request_correct("UnmatchedQty", qty, route, ))
    except Exception:
        basic_custom_actions.create_event('Fail direct_moc_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def direct_child_care_order(qty, route, recipient, count):
    try:
        call(Stubs.win_act_order_book.orderBookDirectChildCare,
             direct_child_care_сorrect('UnmatchedQty', qty, recipient, route, count))
    except Exception:
        basic_custom_actions.create_event('Fail direct_child_care_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def reject_order(lookup, qty, price):
    try:
        call(Stubs.win_act.rejectOrder, reject_order_request(lookup, qty, price))
    except Exception:
        basic_custom_actions.create_event('Fail reject_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def direct_order(lookup, qty, price, qty_percent):
    try:
        call(Stubs.win_act.Direct, direct_order_request(lookup, qty, price, qty_percent))
    except Exception:
        basic_custom_actions.create_event('Fail direct_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def cancel_order(request):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(request)
    cancel_order_details.set_cancel_children(True)
    try:
        call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail cancel_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def split_limit_order(request, qty, type, price, display_qty=None):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    order_split_limit.set_order_type(type)
    order_split_limit.set_limit(price)
    if display_qty is not None:
        order_split_limit.set_display_qty(display_qty)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split_limit)

    try:
        call(Stubs.win_act_order_book.splitLimit, amend_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail split_limit_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def split_order(request, qty, type, price):
    order_split = OrderTicketDetails()
    order_split.set_quantity(qty)
    order_split.set_order_type(type)
    order_split.set_limit(price)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split)

    try:
        call(Stubs.win_act_order_book.splitOrder, amend_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail split_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def transfer_order(request, user):
    transfer_order_details = TransferOrderDetails()
    transfer_order_details.set_default_params(request)
    transfer_order_details.set_transfer_order_user(user, True)
    try:
        call(Stubs.win_act_order_book.transferOrder, transfer_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail transfer_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def internal_transfer(base_request, transfer_accept: bool = True, order_book_filter=None):
    internal_transfer_details = TransferPoolDetailsCLass()
    if transfer_accept:
        internal_transfer_details.confirm_ticket_accept()
    else:
        internal_transfer_details.cancel_ticket_reject()
    internal_transfer_action = InternalTransferActionDetails(base_request, internal_transfer_details.build())
    if order_book_filter is not None:
        internal_transfer_action.set_filter(order_book_filter)
    try:
        call(Stubs.care_orders_action.internalTransferAction, internal_transfer_action.build())
    except Exception:
        basic_custom_actions.create_event('Fail transfer_order', status="FAIL")
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
        basic_custom_actions.create_event('Fail manual_execution', status="FAIL")
        logger.error("Error execution", exc_info=True)


def complete_order(request):
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.completeOrder, complete_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail complete_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def un_complete_order(request):
    un_complete_order_details = ModifyOrderDetails()
    un_complete_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.unCompleteOrder, un_complete_order_details.build())
    except Exception:
        basic_custom_actions.create_event('Fail un_complete_order', status="FAIL")
        logger.error("Error execution", exc_info=True)


def get_order_value(request, column_name, filter_list=None):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id(column_name)
    if filter_list is not None:
        order_details.set_filter(filter_list)
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    try:
        result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail get_order_id', status="FAIL")
    return result[value.name]


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
        basic_custom_actions.create_event('Fail get_order_id', status="FAIL")
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


def get_basket_value(request, column_name, basket_book_filter: dict = None):
    extract_order_data_details = basket_order_book_wrappers.ExtractOrderDataDetails()
    extract_order_data_details.set_default_params(request)
    extract_order_data_details.set_column_names([column_name])
    if basket_book_filter is not None:
        extract_order_data_details.set_filter(basket_book_filter)
    result = call(Stubs.win_act_basket_order_book.extractOrderData, extract_order_data_details.build())
    return result[column_name]


def base_verifier(case_id, printed_name, expected_value, actual_value,
                  verification_method: VerificationMethod = VerificationMethod.EQUALS):
    verifier = Verifier(case_id)
    verifier.set_event_name("Check: " + printed_name)
    verifier.compare_values(printed_name, expected_value, actual_value, verification_method)
    verifier.verify()


def verify_order_value(request, case_id, column_name, expected_value, is_child=False, order_filter_list: list = None):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id(column_name)
    if order_filter_list is not None:
        order_details.set_filter(order_filter_list)
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    if is_child:
        result = call(Stubs.win_act_order_book.getChildOrdersDetails, order_details.request())
    else:
        result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    base_verifier(case_id, column_name, expected_value, result[value.name])


def verify_execution_value(request, case_id, column_name, expected_value, trades_filter_list=None):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(request)
    execution_details.set_extraction_id(extraction_id)
    if trades_filter_list is not None:
        execution_details.set_filter(trades_filter_list)
    trades_price = ExtractionDetail(column_name, column_name)
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_price])))
    response = call(Stubs.win_act_order_book.getTradeBookDetails, execution_details.request())
    base_verifier(case_id, column_name, expected_value, response[column_name])


def verify_block_value(request, case_id, column_name, expected_value):
    ext_id = "MiddleOfficeExtractionId"
    middle_office_service = Stubs.win_act_middle_office_service
    extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=request)
    extract_request.set_extraction_id(ext_id)
    extraction_detail = ExtractionDetail(column_name, column_name)
    extract_request.add_extraction_details([extraction_detail])
    request = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())
    base_verifier(case_id, column_name, expected_value, request[extraction_detail.name])


def verify_allocate_value(request, case_id, column_name, expected_value, account=None):
    extract_request = AllocationsExtractionDetails(base=request)
    middle_office_service = Stubs.win_act_middle_office_service
    if account is not None:
        extract_request.set_allocations_filter({"Account ID": account})
    extraction_detail = ExtractionDetail(column_name, column_name)
    order_details = extract_request.add_order_details()
    order_details.add_extraction_details([extraction_detail])
    result = call(middle_office_service.extractAllocationsTableData, extract_request.build())
    base_verifier(case_id, column_name, expected_value, result[extraction_detail.name])


def verify_basket_value(request, case_id, column_name, expected_value, basket_book_filter=None):
    extract_order_data_details = basket_order_book_wrappers.ExtractOrderDataDetails()
    extract_order_data_details.set_default_params(request)
    extract_order_data_details.set_column_names([column_name])
    if basket_book_filter is not None:
        extract_order_data_details.set_filter(basket_book_filter)
    result = call(Stubs.win_act_basket_order_book.extractOrderData, extract_order_data_details.build())
    base_verifier(case_id, column_name, expected_value, result[column_name])


def notify_dfd(request):
    notify_dfd_request = ModifyOrderDetails()
    notify_dfd_request.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.notifyDFD, notify_dfd_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail notify_dfd', status="FAIL")


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
        basic_custom_actions.create_event('Fail group_modify', status="FAIL")


def reassign_order(request, recipient):
    reassign_order_details = ReassignOrderDetails()
    reassign_order_details.base.CopyFrom(request)
    reassign_order_details.desk = recipient
    try:
        call(Stubs.win_act_order_book.reassignOrder, reassign_order_details)
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail reassign_order', status="FAIL")


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
               remove_fees=False, selected_row_count=None):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    if selected_row_count is not None:
        modify_request.set_selected_row_count(selected_row_count)
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
        response = check_booking_toggle_manual(request)
        if response['book.manualCheckboxState'] == 'unchecked':
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
    extraction_details.extract_net_price("book.totalAllocQty")
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
        basic_custom_actions.create_event('Fail book_order', status="FAIL")


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
        basic_custom_actions.create_event('Fail amend_block', status="FAIL")


def unbook_order(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.unBookOrder, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail amend_block', status="FAIL")


def allocate_order(request, arr_allocation_param: [] = None):
    modify_request = ModifyTicketDetails(base=request)
    allocations_details = modify_request.add_allocations_details()
    '''
    example of arr_allocation_param:
   param=[{"Security Account": "YM_client_SA1", "Alloc Qty": "200"},
           {"Security Account": "YM_client_SA2", "Alloc Qty": "200"}]
    '''
    if arr_allocation_param is not None:
        for i in arr_allocation_param:
            allocations_details.add_allocation_param(i)
    extraction_details = modify_request.add_extraction_details()
    extraction_details.extract_agreed_price("alloc.agreedPrice")
    extraction_details.extract_gross_amount("alloc.grossAmount")
    extraction_details.extract_total_comm("alloc.totalComm")
    extraction_details.extract_total_fees("alloc.totalFees")
    extraction_details.extract_net_price("alloc.netPrice")
    extraction_details.extract_net_amount("alloc.netAmount")

    try:
        response = call(Stubs.win_act_middle_office_service.allocateMiddleOfficeTicket, modify_request.build())
        return response
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail allocate_order', status="TRUE")


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
        for i in range(4):
            misc_details.set_bo_field_1(misc_arr[i])
    extraction_details = modify_request.add_extraction_details()
    extraction_details.extract_agreed_price("alloc.agreedPrice")
    extraction_details.extract_gross_amount("alloc.grossAmount")
    extraction_details.extract_total_comm("alloc.totalComm")
    extraction_details.extract_total_fees("alloc.totalFees")
    extraction_details.extract_net_price("alloc.netPrice")
    extraction_details.extract_net_amount("alloc.netAmount")
    try:
        return call(Stubs.win_act_middle_office_service.amendAllocations, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail amend_allocate', status="FAIL")


def unallocate_order(request):
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(Stubs.win_act_middle_office_service.unAllocateMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail unallocate_order', status="FAIL")


def check_in_order(request):
    order_book_obj = ModifyOrderDetails()
    order_book_obj.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.checkInOrder, order_book_obj.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail check_in_order', status="FAIL")


def check_out_order(request):
    order_book_obj = ModifyOrderDetails()
    order_book_obj.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.checkOutOrder, order_book_obj.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail check_out_order', status="FAIL")


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
        basic_custom_actions.create_event('Fail view_orders_for_block', status="FAIL")


def check_error_in_book(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(request)
    modify_request.set_partial_error_message("error_in_book")
    try:
        error = call(middle_office_service.bookOrder, modify_request.build())
        return error
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail check_error_in_book', status="FAIL")


def re_order_leaves(request, is_sall=False):
    order_ticket = OrderTicketDetails()
    if is_sall:
        order_ticket.sell()
    else:
        order_ticket.buy()
    new_order_details = NewOrderDetails()
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.reOrderLeaves, order_ticket.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail re_order', status="FAIL")


def re_order(request, is_sall=False):
    order_ticket = OrderTicketDetails()
    if is_sall:
        order_ticket.sell()
    else:
        order_ticket.buy()
    new_order_details = NewOrderDetails()
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(request)
    try:
        call(Stubs.win_act_order_book.reOrder, order_ticket.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    basic_custom_actions.create_event('Fail re_order', status="FAIL")


def cancel_execution(request, trades_filter_list=None):
    cancel_manual_execution_details = trades_blotter_wrappers.CancelManualExecutionDetails()
    cancel_manual_execution_details.set_default_params(request)
    cancel_manual_execution_details.set_filter(trades_filter_list)
    call(Stubs.win_act_trades.cancelManualExecution, cancel_manual_execution_details.build())


def approve_block(request):
    middle_office_service = Stubs.win_act_middle_office_service
    modify_request = ModifyTicketDetails(base=request)
    try:
        call(middle_office_service.approveMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail approve_block', status="FAIL")


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
    try:
        return call(middle_office_service.amendMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail amend_block', status="FAIL")


def is_menu_item_present(request, menu_item, filter=None):
    menu_item_details = MenuItemDetails(request)
    menu_item_details.set_menu_item(menu_item)
    if filter is not None:
        menu_item_details.set_filter(filter)
    try:
        return call(Stubs.win_act_order_book.isMenuItemPresent, menu_item_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail is_menu_item_present', status="FAIL")


def manual_match(request, qty_to_match, order_filter_list=None, trades_filter_list=None):
    match_details = MatchDetails()
    if order_filter_list is not None:  # example["Client Name", 'CLIENT1', "OrderId", "CO1210526150717138001"]
        match_details.set_filter(order_filter_list)
    match_details.set_qty_to_match(qty_to_match)
    # match_details.click_cancel()
    match_details.click_match()
    trades_order_details = ModifyTradesDetails(match_details=match_details)
    trades_order_details.set_default_params(request)
    if trades_filter_list is not None:
        trades_order_details.set_filter(trades_filter_list)  # example ["ExecID", 'EX1210616111101191001']
    try:
        call(Stubs.win_act_trades.manualMatch, trades_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail manual_match', status="FAIL")


def get_2nd_lvl_order_detail(request, column_name, row_number: int = 0):
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    lvl_2_detail = ExtractionDetail(column_name, column_name)
    lvl2ext_action = ExtractionAction.create_extraction_action(
        extraction_details=[lvl_2_detail])
    lvl_2_info = OrderInfo.create(actions=[lvl2ext_action], row_number=row_number)
    sub_order_details = OrdersDetails.create(order_info_list=[lvl_2_info])
    main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action,
                                                              sub_order_details=sub_order_details))
    try:
        request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail get_2nd_lvl_order_detail', status="FAIL")
    return request[column_name]


def suspend_order(base_request, cancel_children=False, filter=None):
    suspend_order_details = SuspendOrderDetails(base_request)
    if filter is not None:
        suspend_order_details.set_filter(filter)
    suspend_order_details.set_cancel_children(cancel_children)
    try:
        call(Stubs.win_act_order_book.suspendOrder, suspend_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail suspend_order', status="FAIL")


def release_order(base_request, filter=None):
    base_order_details = BaseOrdersDetails(base_request)
    if filter is not None:
        base_order_details.set_filter(filter)
    try:
        call(Stubs.win_act_order_book.releaseOrder, base_order_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail release_order', status="FAIL")


def add_to_basket(request, list_row_numbers: [], basket_name=""):
    add_to_basket_details = AddToBasketDetails(request, list_row_numbers, basket_name)
    try:
        call(Stubs.win_act_order_book.addToBasket, add_to_basket_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail add_to_basket', status="FAIL")


def add_basket_template(request, client, templ_name, descrip, tif='Day', exec_policy='Care', symbol_source='ISIN',
                        has_header=True, templ: {} = None):
    if templ is None:
        templ = {'Symbol': ['1', 'FR0004186856'], 'Quantity': ['2', '0'], 'Price': ['3', '0'],
                 'Account': ['4', 'CLIENT_FIX_CARE_SA1'], 'Side': ['5', 'Buy'], 'OrdType': ['6', 'Limit'],
                 'StopPrice': ['7', '0'], 'Capacity': ['8', 'Agency']}

    fields_details = [
        ImportedFileMappingFieldDetails(ImportedFileMappingField.SYMBOL, templ.get('Symbol')[0],
                                        templ.get('Symbol')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.QUANTITY, templ.get('Quantity')[0],
                                        templ.get('Quantity')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.PRICE, templ.get('Price')[0],
                                        templ.get('Price')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.SIDE, templ.get('Side')[0],
                                        templ.get('Side')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.ORD_TYPE, templ.get('OrdType')[0],
                                        templ.get('OrdType')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.STOP_PRICE, templ.get('StopPrice')[0],
                                        templ.get('StopPrice')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.ACCOUNT, templ.get('Account')[0],
                                        templ.get('Account')[1]).build(),
        ImportedFileMappingFieldDetails(ImportedFileMappingField.CAPACITY, templ.get('Capacity')[0],
                                        templ.get('Capacity')[1]).build()
    ]
    details = ImportedFileMappingDetails(has_header, fields_details).build()
    templates_details = TemplatesDetails()
    templates_details.set_default_params(request)
    templates_details.set_name_value(templ_name)
    templates_details.set_exec_policy(exec_policy)
    templates_details.set_default_client(client)
    templates_details.set_description(descrip)
    templates_details.set_symbol_source(symbol_source)
    templates_details.set_time_in_force(tif)
    templates_details.set_imported_file_mapping_details(details)
    try:
        call(Stubs.win_act_basket_ticket.manageTemplates, templates_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail add_to_basket', status="FAIL")


def basket_row_details(row, remove_row=False, symbol=None, side=None, ord_type=None, capacity=None):
    if not remove_row:
        params = {}
        if symbol is not None:
            params.update({'Symbol': symbol})
        if side is not None:
            params.update({'Side': symbol})
        if ord_type is not None:
            params.update({'Order Type': ord_type})
        if capacity is not None:
            params.update({'Capacity': capacity})
        result = RowDetails(row, False, params).build()
    else:
        RowDetails(row, True).build()
    return result


def create_basket_via_import(request, basket_name, basket_template_name, path, client=None, expire_date=None, tif=None,
                             is_csv=False, amend_rows_details: [basket_row_details] = None):
    if is_csv:
        file_type = FileType.CSV
    else:
        file_type = FileType.EXCEL
    file_details = FileDetails(0, path).build()
    basket_ticket_details = BasketTicketDetails()
    basket_ticket_details.set_file_details(file_details)
    basket_ticket_details.set_default_params(request)
    basket_ticket_details.set_name_value(basket_name)
    basket_ticket_details.set_basket_template_name(basket_template_name)
    basket_ticket_details.set_client_value(client)
    if expire_date is not None:
        basket_ticket_details.set_date_value(expire_date)
    if tif is not None:
        basket_ticket_details.set_time_in_force_value(tif)
    if amend_rows_details is not None:
        basket_ticket_details.set_row_details(amend_rows_details)
    # try:
    call(Stubs.win_act_basket_ticket.createBasketViaImport, basket_ticket_details.build())
    # except Exception:
    # logger.error("Error execution", exc_info=True)
    # basic_custom_actions.create_event('Fail create_basket_via_import', status="FAIL")
