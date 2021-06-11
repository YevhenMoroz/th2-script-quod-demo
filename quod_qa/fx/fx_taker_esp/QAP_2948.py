import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, \
    ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails

from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    call(service.placeESPOrder, esp_request.build())


def check_stop_price_in_ord_t(base_request, service, case_id):
    extract_value = ExtractFxOrderTicketValuesRequest(base_request)
    extract_value.get_stop_price("orderTicket.StopPrice")
    extract_value.get_price_large("orderTicket.PriceLarge")
    extract_value.get_price_pips("orderTicket.PricePips")
    response = call(service.extractFxOrderTicketValues, extract_value.build())
    extracted_stop_price = response["orderTicket.StopPrice"]
    price = response["orderTicket.PriceLarge"] + response["orderTicket.PricePips"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check stop price in order ticket")
    verifier.compare_values("Stop price", "", extracted_stop_price)
    verifier.verify()
    return price


def send_order(base_request, service, order_type, tif, stop_price):
    order_ticket = FXOrderDetails()
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    order_ticket.set_stop_price(stop_price)
    order_ticket.set_slippage("0")
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def check_order_book(base_request, act_ob, case_id, owner, stop_price, price):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Owner", owner])
    ob_order_type = ExtractionDetail("orderBook.orderType", "OrdType")
    ob_exec_policy = ExtractionDetail("orderBook.execPolicy", "ExecPcy")
    ob_stop_price = ExtractionDetail("orderBook.stopPrice", "StpPx")
    ob_free_notes = ExtractionDetail("orderBook.freeNotes", "FreeNotes")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_order_type,
                                                                                 ob_exec_policy,
                                                                                 ob_stop_price,
                                                                                 ob_free_notes])))

    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("OrderType", "StopLimit", response[ob_order_type.name])
    verifier.compare_values("Exec Policy", "Synth (Quod MultiListing)", response[ob_exec_policy.name])
    verifier.compare_values("Stop Price", stop_price, response[ob_stop_price.name])
    verifier.compare_values("Free notes", "11605 'StopPrice' (2) greater than 'Price' (" + price + ")",
                            response[ob_free_notes.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    ord_type = "Limit"
    tif = "Day"
    stop_price = "2"
    owner = Stubs.custom_config['qf_trading_fe_user_309']

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        place_order(base_esp_details, ar_service)
        # Step 2
        price = check_stop_price_in_ord_t(base_tile_data, order_ticket_service, case_id)
        send_order(case_base_request, order_ticket_service, ord_type, tif, stop_price)
        close_order_ticket(case_base_request, order_ticket_service)
        # Step 3
        check_order_book(case_base_request, ob_service, case_id, owner, stop_price, price)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
