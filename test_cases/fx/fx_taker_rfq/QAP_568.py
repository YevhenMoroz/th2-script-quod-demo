import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.win_gui_wrappers.data_set import Side
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile
from stubs import Stubs
from win_gui_modules.layout_panel_wrappers import OptionOrderTicketRequest, DefaultFXValues
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def set_order_ticket_options(option_service, base_request, client):
    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    fx_values = DefaultFXValues([])
    fx_values.Client = client
    order_ticket_options.set_default_fx_values(fx_values)
    call(option_service.setOptionOrderTicket, order_ticket_options.build())


# @decorator_try_except(test_id=Path(__file__).name[:-3])
def execute(report_id, session_id):
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
    sell_side = Side.sell.value

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:
        # Step 1-3
        set_order_ticket_options(option_service, case_base_request, case_client)
        # Step 4
        rfq_tile = RFQTile(case_id, session_id)
        rfq_tile.crete_tile().modify_rfq_tile(from_cur=case_from_currency, to_cur=case_to_currency,
                                              near_qty=case_qty, near_tenor=case_near_tenor,
                                              client=case_client, single_venue=case_venue)
        rfq_tile.send_rfq()
        quote_request_book = FXQuoteRequestBook(case_id, session_id)
        quote_request_book.set_filter(["Qty", case_qty])
        quote_request_book.check_quote_book_fields_list({"Venue": case_venue,
                                                         "Status": quote_sts_new,
                                                         "QuoteStatus": quote_sts_accepted})
        # Step 5
        rfq_tile.place_order(sell_side)

        quote_id = FXOrderBook(case_id, session_id).set_filter(["Qty", case_qty]).extract_field("QuoteID")

        order_book = FXOrderBook(case_id, session_id)
        order_book.check_order_fields_list({"ExecSts": "Filled", "Client ID": case_client})

        quote_book = FXQuoteBook(case_id, session_id)
        quote_book.set_filter(["Id", quote_id]).check_quote_book_fields_list(
            {"QuoteStatus": "Terminated", "Owner": quote_owner})

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            rfq_tile.close_tile()
        except Exception:
            logging.error("Error execution", exc_info=True)
