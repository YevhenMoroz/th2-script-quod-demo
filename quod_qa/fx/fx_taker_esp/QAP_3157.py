import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, \
    FXOrdersDetails, FXOrderInfo
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def open_order_ticket(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def place_order(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_care_order("Aspect Desk Of Traders (CN)", False)
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def check_order_book(base_request, act_ob, case_id, owner, status):
    ob = FXOrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Owner", owner])
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob.add_single_order_info(
        FXOrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_sts])))

    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Sts", status, response[ob_sts.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_service = Stubs.win_act_order_book_fx
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    curr_eur = "EUR"
    curr_usd = "USD"
    tenor = "Spot"
    owner = Stubs.custom_config['qf_trading_fe_user']
    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, curr_eur, curr_usd, tenor)
        open_order_ticket(base_esp_details, ar_service)
        place_order(case_base_request, order_ticket_service)
        check_order_book(case_base_request, ob_service, case_id, owner, "Sent")
        # Step 2
        time.sleep(15)
        check_order_book(case_base_request, ob_service, case_id, owner, "Rejected")

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
