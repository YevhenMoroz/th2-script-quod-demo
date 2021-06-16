import logging

from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base

from quod_qa.fx.ui_test_ex import extract_error_message_order_ticket
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_4297"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket

    lookup = "RELIANCE"
    # "0-111111111" using to bypass the inability to enter a minus after clearing a "Price" field
    price = ["0", "0-111111111", "10", "abc"]
    stop_price = ["20", "abc"]
    qty = "400"
    client = "HAKKIM"
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
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[0])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Rejected")
    eq_wrappers.verify_value(base_request, case_id, "FreeNotes", "11603 'Price' (0) negative or zero")
    # endregion

    # region Create 2nd order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[1])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Rejected")
    eq_wrappers.verify_value(base_request, case_id, "FreeNotes", "11603 'Price' (-99999999) negative or zero")
    # endregion

    # region Create 3rd order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[2])
    order_ticket.set_stop_price(stop_price[0])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Rejected")
    eq_wrappers.verify_value(base_request, case_id, "FreeNotes", "11605 'StopPrice' (20) greater than 'Price' (10)")
    # endregion

    # region Create 4th order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_instrument(symbol)
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price[3])
    order_ticket.set_stop_price(stop_price[1])
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(order_ticket_service.setOrderDetails, new_order_details.build())
    # error extraction
    extract_error_message_order_ticket(base_request, order_ticket_service)
    # end region

    # region Check values in OrderBook
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Rejected")
    eq_wrappers.verify_value(base_request, case_id, "FreeNotes", "11603 'Price' (0) negative or zero")
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
