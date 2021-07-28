import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest, \
    SelectRowsRequest, DeselectRowsRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def select_rows(base_request, cp_service, row_numbers):
    request = SelectRowsRequest(base_request)
    request.set_row_numbers(row_numbers)
    call(cp_service.selectRows, request.build())


def deselect_rows(base_request, cp_service):
    request = DeselectRowsRequest(base_request)
    call(cp_service.deselectRows, request.build())


def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())


def press_executable(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_executable()
    call(service.modifyRatesTile, modify_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def place_order(base_request, service, client, slippage, qty):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.set_quantity(qty)
    place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def check_order_book(base_request, act_ob, instr_type, case_id, qty, owner, client, free_notes, status):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Owner", owner, "Client ID", client])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_sts = ExtractionDetail("orderBook.execsts", "Sts")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob_free_notes = ExtractionDetail("orderbook.freenotes", "FreeNotes")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_sts,
                                                                                 ob_qty,
                                                                                 ob_free_notes])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("InstrType", instr_type, response[ob_instr_type.name])
    verifier.compare_values("Sts", status, response[ob_sts.name])
    verifier.compare_values("Qty", qty, response[ob_qty.name].replace(',', ''))
    verifier.compare_values("Free notes", free_notes, response[ob_free_notes.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-SPOT"
    client_tier = "Silver"
    client = "Silver1"
    slippage = "10"
    instrument_type = "Spot"
    qty_1m = "1000000"
    qty_2m = "2000000"
    owner = Stubs.custom_config['qf_trading_fe_user']
    empty_free_notes = ""
    pricing_off = "not active"
    executable_off = "not tradeable"
    notes = "not enough quantity in book"
    sts_rej = "Rejected"
    sts_term = "Terminated"

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
        press_pricing(base_details, cp_service)
        select_rows(base_details, cp_service, [1, 2])
        press_executable(base_details, cp_service)
        # Step 7
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, empty_free_notes, sts_term)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, notes, sts_rej)
        # Step 8
        press_pricing(base_details, cp_service)
        press_executable(base_details, cp_service)
        # Step 9
        place_order(base_details, cp_service, client, slippage, qty_1m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_1m, owner, client, empty_free_notes, sts_term)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, notes, sts_rej)
        # Step 10
        press_pricing(base_details, cp_service)
        place_order(base_details, cp_service, client, slippage, qty_2m)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty_2m, owner, client, empty_free_notes, sts_term)

        use_default(base_details, cp_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
