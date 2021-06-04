import logging

from datetime import datetime
from th2_grpc_act_gui_quod.order_ticket_pb2 import ExtractOrderTicketValuesRequest
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# wrapper for errors extracting
# def extract_error_message_order_ticket(base_request, order_ticket_service):
#     # extract rates tile table values
#     extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
#     extract_errors_request.extract_error_message()
#     result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
#     print(result)


def execute(report_id):
    case_name = "RIN_1144"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = ["100", "1234567891011", "200"]
    price = ["1234567,89", "100"]
    client = ["HAKKIM", " "]
    lookup = "RELIANCE"
    symbol = "RELIANCE"
    # endregion

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
    # endregion

    # region Create 1st order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty[0])
    order_ticket.set_limit(price[0])
    order_ticket.set_client(client[0])
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())

    # extract_error_message_order_ticket(base_request, order_ticket_service) - replace code bellow with this
    error_message_value = ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
    error_message_value.type = ExtractOrderTicketValuesRequest.OrderTicketExtractedType.ERROR_MESSAGE
    error_message_value.name = "ErrorMessage"

    request = ExtractOrderTicketValuesRequest()
    request.base.CopyFrom(base_request)
    request.extractionId = "ErrorMessageExtractionID"
    request.extractedValues.append(error_message_value)
    call(Stubs.win_act_order_ticket.extractOrderTicketErrors, request)
    # end region

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Status", order_status.name, "Open")]))
    # endregion

    # region Create 2nd order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty[1])
    order_ticket.set_limit(price[1])
    order_ticket.set_client(client[0])
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())

    error_message_value = ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
    error_message_value.type = ExtractOrderTicketValuesRequest.OrderTicketExtractedType.ERROR_MESSAGE
    error_message_value.name = "ErrorMessage"

    request = ExtractOrderTicketValuesRequest()
    request.base.CopyFrom(base_request)
    request.extractionId = "ErrorMessageExtractionID"
    request.extractedValues.append(error_message_value)
    call(Stubs.win_act_order_ticket.extractOrderTicketErrors, request)
    # end region

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Status", order_status.name, "Open")]))
    # endregion

    # region Create 3rd order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty[2])
    order_ticket.set_limit(price[1])
    order_ticket.set_client(client[1])
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())

    error_message_value = ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
    error_message_value.type = ExtractOrderTicketValuesRequest.OrderTicketExtractedType.ERROR_MESSAGE
    error_message_value.name = "ErrorMessage"

    request = ExtractOrderTicketValuesRequest()
    request.base.CopyFrom(base_request)
    request.extractionId = "ErrorMessageExtractionID"
    request.extractedValues.append(error_message_value)
    call(Stubs.win_act_order_ticket.extractOrderTicketErrors, request)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
