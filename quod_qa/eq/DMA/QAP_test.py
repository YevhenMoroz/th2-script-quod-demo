import logging

from datetime import datetime

from th2_grpc_act_gui_quod.order_ticket_pb2 import ExtractOrderTicketValuesRequest

from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_test"
    seconds, nanos = timestamps()  # Store case start tim
    # region Declarations

    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    symbol = "ACC-A"
    qty = "0"
    price = "3"
    client = "HAKKIM"
    lookup = "TCS"
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

  # region Create order via FE

    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.set_tif("Day")
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


    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, request)
    print(result)

    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.set_tif("Day")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())


    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
