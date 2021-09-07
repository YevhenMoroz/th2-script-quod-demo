from datetime import datetime
from urllib import request

from th2_grpc_act_gui_quod import act_ui_win_pb2
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest
from th2_grpc_act_gui_quod.order_book_pb2 import TransferOrderDetails, NotifyDfdDetails, ExtractManualCrossValuesRequest
from copy import deepcopy
from custom import basic_custom_actions
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest, \
    ExtractOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe, call
from win_gui_modules.wash_book_positions_wrappers import GetWashBookDetailsRequest, \
    ExtractionWashBookPositionsFieldsDetails, WashPositionsInfo, ExtractionWashBookPositionsAction
from win_gui_modules.wrappers import set_base, accept_order_request, direct_order_request, reject_order_request, \
    direct_loc_request_correct, direct_moc_request_correct, direct_poc_request_correct, BaseParams
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails, \
    ManualCrossDetails, ManualExecutingDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request


def open_fe(session_id, report_id, case_id, folder, user, password):
    init_event = create_event("Initialization", parent_id=report_id)
    set_base(session_id, case_id)
    if not Stubs.frontend_is_open:
        prepare_fe(init_event, session_id, folder, user, password)
    else:
        get_opened_fe(case_id, session_id)


def create_order(base_request, qty, client, lookup, order_type, tif="Day", is_care=False, recipient=None,
                 price=None, washbook=None,
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
    if washbook is not None:
        order_ticket.set_washbook(washbook)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())


def extract_error_message_order_ticket(base_request, order_ticket_service):

    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
    return result


def check_order_benchmark_book(base_request, case_id, ob_act, order_id, column_name, expected_value):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_filter(["Order ID", order_id])
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    sub_order_ob_par_name = ExtractionDetail("Benchmarks.Status", "Status")
    lvl1_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=
                                                                                  [sub_order_ob_par_name]))
    lvl1_details = OrdersDetails.create(info=lvl1_info)
    ob.add_single_order_info(OrderInfo.create(sub_order_details=lvl1_details))
    response = call(ob_act.getBenchmarkTabDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values(column_name, expected_value, response[sub_order_ob_par_name.name])
    verifier.verify()
    print(response)


def cancel_negative_ex(base_request, order_book_service):

    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.cancel_by_icon()
    call(order_book_service.cancelOrder, cancel_order_details.build())


def amend_negative_ex(base_request, order_book_service):

    order_amend = OrderTicketDetails()
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_order_details(order_amend)
    amend_order_details.set_default_params(base_request)
    amend_order_details.amend_by_icon()
    call(order_book_service.amendOrder, amend_order_details.build())


def create_order_extracting_error(base_request, qty, client, lookup, tif, side, order_type=None, price=None,
                                  pos_validity=None):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_instrument(lookup)
    order_ticket.set_tif(tif)
    if pos_validity:
        order_ticket.set_general_tab_in_advanced(pos_validity)
    if order_type:
        order_ticket.set_order_type(order_type)
        order_ticket.set_limit(price)
    if side == "Buy":
        order_ticket.buy()
    if side == "Sell":
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.setOrderDetails, new_order_details.build())


def accept_order(lookup, qty, price):
    call(Stubs.win_act.acceptOrder, accept_order_request(lookup, qty, price))


def accept_modify(lookup, qty, price):
    call(Stubs.win_act.acceptModifyPlusChild, accept_order_request(lookup, qty, price))


def direct_loc_order(qty_percentage, route):
    call(Stubs.win_act_order_book.orderBookDirectLoc, direct_loc_request_correct("UnmatchedQty", qty_percentage, route))


def direct_moc_order(qty_percentage, route):
    call(Stubs.win_act_order_book.orderBookDirectMoc, direct_moc_request_correct("UnmatchedQty", qty_percentage, route))


def direct_poc_order(reference_price, percentage, qty_percentage, route):
    call(Stubs.win_act_order_book.orderBookDirectPoc, direct_poc_request_correct("UnmatchedQty", reference_price,
                                                                                 percentage, qty_percentage, route))


def direct_poc_order_via_inbox(reference_price, percentage, qty_percentage, route):
    call(Stubs.win_act.clientInboxDirectPoc, direct_poc_request_correct("UnmatchedQty", reference_price,
                                                                        percentage, qty_percentage, route))


def direct_child_care_order(qty_percentage, route, recipient):
    call(Stubs.win_act_order_book.orderBookDirectChildCare, direct_moc_request_correct("UnmatchedQty", qty_percentage,
                                                                                       route, recipient))


def direct_poc_error_extraction(reference_price, percentage, qty_percentage, route):
    error_message = ExtractDirectsValuesRequest.DirectsExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractDirectsValuesRequest.DirectsExtractedType.ERROR_MESSAGE
    request = ExtractDirectsValuesRequest()
    request.extractionId = "DirectErrorMessageExtractionID"
    request.extractedValues.append(error_message)
    response = call(Stubs.win_act_order_book.orderBookDirectPoc,
                    direct_poc_request_correct('UnmatchedQty', reference_price, percentage, qty_percentage, route))
    print(response)


def reject_order(lookup, qty, price):
    call(Stubs.win_act.rejectOrder, reject_order_request(lookup, qty, price))


def direct_order(lookup, qty, price, qty_percent):
    call(Stubs.win_act.Direct, direct_order_request(lookup, qty, price, qty_percent))


def amend_order(request, order_id, client=None, qty=None, price=None, account=None):
    order_amend = OrderTicketDetails()
    if qty is not None:
        order_amend.set_quantity(qty)
    if price is not None:
        order_amend.set_limit(price)
    if client is not None:
        order_amend.set_client(client)
    if account is not None:
        order_amend.set_account(account)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_filter(["Order ID", order_id])
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_amend)
    call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())


def cancel_order(request):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(request)
    cancel_order_details.set_cancel_children(True)
    call(Stubs.win_act_order_book.cancelOrder, cancel_order_details.build())


def complete_order(request, order_id):
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(request)
    complete_order_details.set_filter(["Order ID", order_id])
    call(Stubs.win_act_order_book.completeOrder, complete_order_details.build())


def split_limit_order(request, qty, order_type):
    order_split_limit = OrderTicketDetails()
    order_split_limit.set_quantity(qty)
    order_split_limit.set_order_type(order_type)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(request)
    amend_order_details.set_order_details(order_split_limit)
    call(Stubs.win_act_order_book.splitLimit, amend_order_details.build())


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


def switch_user(session_id, case_id):
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    Stubs.win_act.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)


def verify_order_value(request, case_id, column_name, expected_value, is_child):
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


def get_wash_book_positions_details(security_account, column_name, act, base_request):
    dealing_positions_details = GetWashBookDetailsRequest()
    extraction_id_wash_book = "Wash Book Position"
    dealing_positions_details.set_default_params(base_request)
    dealing_positions_details.set_security_account(security_account)
    dealing_positions_details.set_extraction_id(extraction_id_wash_book)
    value = ExtractionWashBookPositionsFieldsDetails(column_name, column_name)

    dealing_positions_details.add_single_positions_info(
        WashPositionsInfo.create(
            action=ExtractionWashBookPositionsAction.create_extraction_action(
                extraction_details=[value])))

    response = call(act.getWashBookPositionsDetails, dealing_positions_details.request())
    return response[column_name]


def extract_parent_order_details(base_request, column_name, extraction_id, order_id):
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    order_details.set_filter(['Order ID', order_id])
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[column_name]


def extract_child_lvl1_order_details(base_request, column_name, extraction_id, child_order_id=None):
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(extraction_id)
    if child_order_id:
        child_main_order_details.set_filter(['Order ID', child_order_id])
    value = ExtractionDetail(column_name, column_name)
    sub_lvl1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[value])

    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action])
    sub_order_details_level1 = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details_level1))

    request = call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())
    return request[column_name]


def extract_child_lvl2_order_details(base_request, column_name, order_book_service, parent_order_id, extraction_id):
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    order_details.set_filter(['ParentOrdID', parent_order_id])

    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    request = call(order_book_service.getChildOrdersDetails, order_details.request())
    return request[column_name]


def verifier(case_id, event_name, expected_value, actual_value):
    # region verifier
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Value")
    verifier.compare_values(event_name, expected_value, actual_value)
    verifier.verify()
