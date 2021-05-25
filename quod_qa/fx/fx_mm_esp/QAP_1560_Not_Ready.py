import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())

def modify_rates_tile(base_request, service, instrument, client, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    modify_request.set_pips(pips)
    call(service.modifyRatesTile, modify_request.build())

def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())

def press_use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())

def modify_spread(base_request, service, *args):
    modify_request = ModifyRatesTileRequest(details=base_request)
    if "increase_ask" in args:
        modify_request.increase_ask()
    if "decrease_ask" in args:
        modify_request.decrease_ask()
    if "increase_bid" in args:
        modify_request.increase_bid()
    if "decrease_bid" in args:
        modify_request.decrease_bid()
    if "narrow_spread" in args:
        modify_request.narrow_spread()
    if "widen_spread" in args:
        modify_request.widen_spread()
    if "skew_towards_ask" in args:
        modify_request.skew_towards_ask()
    if "skew_towards_bid" in args:
        modify_request.skew_towards_bid()
    call(service.modifyRatesTile, modify_request.build())









def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-SPOT"
    client_tier = "Silver"
    client = "Silver1"
    slippage = "2"
    instrument_type = "Spot"
    qty_1m = "1000000"
    qty_2m = "2000000"
    owner = "ostronov"
    empty_free_notes = ""
    pricing_off = "not active"
    executable_off = "not tradeable"
    sts_rej = "Rejected"
    sts_term = "Terminated"

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        # Step 2
        press_executable(base_details, cp_service)
        # Step 3
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, executable_off, sts_rej)
        # Step 4
        press_executable(base_details, cp_service)
        press_pricing(base_details, cp_service)
        # Step 5
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, pricing_off, sts_rej)
        # Step 6
        # TODO Need to select row
        press_pricing(base_details, cp_service)
        press_executable(base_details, cp_service)
        # Step 7
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, empty_free_notes, sts_term)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, executable_off, sts_rej)
        # Step 8
        press_pricing(base_details, cp_service)
        press_executable(base_details, cp_service)
        # Step 9
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, empty_free_notes, sts_term)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, pricing_off, sts_rej)
        # Step 10
        press_pricing(base_details, cp_service)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, empty_free_notes, sts_term)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # Close tile
        call(cp_service.closeWindow, case_base_request)
