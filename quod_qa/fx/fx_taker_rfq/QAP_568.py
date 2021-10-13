import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from quod_qa.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import OptionOrderTicketRequest, DefaultFXValues
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, client, tenor, venue):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity_as_string(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    action = ContextAction.create_venue_filter(venue)
    modify_request.add_context_action(action)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.SELL)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def set_order_ticket_options(option_service, base_request, client):
    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    fx_values = DefaultFXValues([])
    fx_values.Client = client
    order_ticket_options.set_default_fx_values(fx_values)
    call(option_service.setOptionOrderTicket, order_ticket_options.build())


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    option_service = Stubs.win_act_options

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_venue = "CITI"

    case_qty = random_qty(1, 3, 7)
    quote_sts_new = "New"
    quote_sts_accepted = "Accepted"
    quote_owner = Stubs.custom_config['qf_trading_fe_user']

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1-3
        set_order_ticket_options(option_service, case_base_request, case_client)
        # Step 4
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                        case_client, case_near_tenor, case_venue)
        send_rfq(base_rfq_details, ar_service)
        quote_request_book = FXQuoteRequestBook(case_id, case_base_request)
        quote_request_book.set_filter(["Qty", "10000000"])
        quote_request_book.check_quote_book_fields_list({"Venue": case_venue,
                                                         "Status": quote_sts_new,
                                                         "QuoteStatus": quote_sts_accepted})
        # Step 5
        place_order_tob(base_rfq_details, ar_service)
        quote_id = FXOrderBook(case_id, case_base_request).set_filter(["Qty", "2368459"]).extract_field("QuoteID")
        order_book = FXOrderBook(case_id, case_base_request)
        order_book.check_order_fields_list({"ExecSts": "Filled", "Client ID": case_client})

        quote_book = FXQuoteBook(case_id, case_base_request)
        quote_book.set_filter(["Id", quote_id]).check_quote_book_fields_list(
            {"QuoteStatus": "Terminated", "Owner": quote_owner})

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
