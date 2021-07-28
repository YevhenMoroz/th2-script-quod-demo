import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    ModifyFXOrderDetails, CancelFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def click_on_ask_btn(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.SELL)
    call(service.placeESPOrder, esp_request.build())


def modify_order_ticket(base_request, service, type, qty, price, tif, client):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_price_large(price)
    order_ticket.set_tif(tif)
    order_ticket.set_order_type(type)
    order_ticket.set_client(client)
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def extract_price_from_order_ticket(tile_date, service):
    extract_request = ExtractFxOrderTicketValuesRequest(tile_date)
    extract_request.get_price_large("priceLarge")
    extract_request.get_price_pips("pricePips")
    response = call(service.extractFxOrderTicketValues, extract_request.build())
    price = response["priceLarge"] + response["pricePips"]
    print(price)
    return price


def place_order(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def amend_order(ob_act, base_request, *args):
    order_details = FXOrderDetails()
    if "price" in args:
        order_details.set_price_large("1.18")
        order_details.set_price_pips("000")
    if "qty" in args:
        order_details.set_qty("8000000")
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_order_details(order_details)

    call(ob_act.amendOrder, modify_ot_order_request.build())


def cancel_order(base_request, ob_act):
    cancel_order_request = CancelFXOrderDetails(base_request)
    call(ob_act.cancelOrder, cancel_order_request.build())


def check_order_book(base_request, act_ob, case_id, owner, qty, sts, price):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner, "Qty", qty])

    child_ord_id = ExtractionDetail("orderBook.childId", "Order ID")
    child_sts = ExtractionDetail("orderBook.childSts", "Sts")
    child_lmt_price = ExtractionDetail("orderBook.childLmtPrice", "Limit Price")
    child_qty = ExtractionDetail("orderBook.childQty", "Qty")

    child_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[child_ord_id,
                                                                                                       child_sts,
                                                                                                       child_lmt_price,
                                                                                                       child_qty]))
    child_details = OrdersDetails.create(info=child_info)

    ob_ord_id = ExtractionDetail("OrderBook.ordId", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_lmt_price = ExtractionDetail("orderBook.lmtPrice", "Limit Price")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[ob_sts, ob_lmt_price, ob_qty, ob_ord_id]),
            sub_order_details=child_details))
    response = call(act_ob.getMyOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Sts", sts, response[ob_sts.name])
    verifier.compare_values("Limit Price", price, response[ob_lmt_price.name])
    verifier.compare_values("Child status", sts, response[child_sts.name])
    verifier.verify()
    main_order_id = response[ob_ord_id.name]
    child_order_id = response[child_ord_id.name]

    return [main_order_id, child_order_id]


def check_order_after_amend(base_request, act_ob, case_id, order_id, qty, sts):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", order_id])

    child_ord_id = ExtractionDetail("orderBook.childId", "Order ID")
    child_sts = ExtractionDetail("orderBook.childSts", "Sts")
    child_qty = ExtractionDetail("orderBook.childQty", "Qty")

    child_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[child_ord_id,
                                                                                                       child_sts,
                                                                                                       child_qty]))
    child_details = OrdersDetails.create(info=child_info)

    ob_ord_id = ExtractionDetail("OrderBook.ordId", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[ob_sts, ob_qty, ob_ord_id]),
            sub_order_details=child_details))
    response = call(act_ob.getMyOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book after Amend")
    verifier.compare_values("Sts", sts, response[ob_sts.name])
    verifier.compare_values("Qty", qty, response[ob_qty.name].replace(",", ""))
    verifier.compare_values("Child status", sts, response[child_sts.name])
    verifier.compare_values("Child Qty", qty, response[child_qty.name].replace(",", ""))
    verifier.verify()
    child_order_id = response[child_ord_id.name]

    return child_order_id


def check_child_book(base_request, act_ob, case_id, order_id):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", order_id])
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_detail=ob_sts)))
    response = call(act_ob.getChildOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check that child is canceled")
    verifier.compare_values("Child status", "Cancelled", response[ob_sts.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_fx_service = Stubs.win_act_order_book_fx
    ob_service = Stubs.win_act_order_book
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_details = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    qty = "10000000"
    price = "1.19"
    tif = "Day"
    order_type = "Limit"
    client = "ASPECT_CITI"
    owner = Stubs.custom_config['qf_trading_fe_user']

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        click_on_ask_btn(base_esp_details, ar_service)
        modify_order_ticket(case_base_request, order_ticket_service, order_type, qty, price, tif, client)
        price_extracted = extract_price_from_order_ticket(base_tile_details, order_ticket_service)
        place_order(case_base_request, order_ticket_service)
        # Step 2-3
        order_info = check_order_book(case_base_request, ob_service, case_id, owner, qty, "Open", price_extracted)
        # Step 4
        amend_order(ob_fx_service, case_base_request, "qty")
        check_child_book(case_base_request, ob_service, case_id, order_info[1])
        check_order_after_amend(case_base_request, ob_service, case_id, order_info[0], "8000000",
                                "Open")
        # Step 5
        cancel_order(case_base_request, ob_service)
        check_order_after_amend(case_base_request, ob_service, case_id, order_info[0], "8000000",
                                "Cancelled")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
