import logging
import random
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ActionsRatesTile,\
                                                      PlaceESPOrder, ESPTileOrderSide

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    ModifyOrderDetails, ModifyFXOrderDetails, ReleaseFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails, OrderTicketDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import (SelectRowsRequest, DeselectRowsRequest, ExtractRatesTileValues,
                                                     PlaceRateTileTableOrderRequest, RatesTileTableOrdSide,
                                                     ExtractRatesTileTableValuesRequest)


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, small, large):
    order_ticket = FXOrderDetails()
    pips_len = str(len(small))
    small = str(int(int(small)-int(50)))
    value = ("{:0"+pips_len+"d}").format(int(small))
    order_ticket.set_price_pips(value)
    order_ticket.set_price_large(large)
    order_ticket.set_place()
    order_ticket.set_strategy('test')
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def extract_price_from_ot(base_request, service):
    order_ticket = ExtractFxOrderTicketValuesRequest(base_request)
    order_ticket.get_price_pips("orderTicket.Pips")
    order_ticket.get_price_large('orderTicket.Large')
    response = call(service.extractFxOrderTicketValues, order_ticket.build())
    return [response['orderTicket.Pips'], response['orderTicket.Large']]


def modify_rates_tile(base_request, service, from_c, to_c, tenor, qty):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    modify_request.set_quantity(qty)
    call(service.modifyRatesTile, modify_request.build())


def check_order_book(base_request, act_ob, case_id, instr_type, owner, qty):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner])
    ob.set_filter(['Qty', qty])
    ob_exec_pcy = ExtractionDetail("orderBook.ExecPolicy", "ExecPcy")
    # ob_cd_sts = ExtractionDetail("orderBook.CSStatus", "CDSts")
    ob_sts = ExtractionDetail("orderBook.Status", "Sts")
    ob_qty = ExtractionDetail('orderBook', 'Qty')
    ob_owner = ExtractionDetail("orderBook.owner", "Owner")
    ob_ord_id = ExtractionDetail('orderBook.OrderId', 'Order ID')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_pcy,
                                                                                 ob_sts,
                                                                                 ob_qty,
                                                                                 ob_owner,
                                                                                 ob_ord_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('ExecPcy', 'Synth (Quod MultiListing)', response[ob_exec_pcy.name])
    verifier.compare_values('Status', 'Open', response[ob_sts.name])
    verifier.compare_values("Owner", owner, response[ob_owner.name])
    verifier.compare_values('Qty', qty, response[ob_qty.name].replace(',', ''))
    verifier.verify()
    print(response[ob_ord_id.name])
    return response[ob_ord_id.name]


def open_order_ticket_via_double_click(ob_act, base_request):
    order_details = FXOrderDetails()
    # order_details.set_qty('123123123')
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_order_details(order_details)
    call(ob_act.openOrderTicketByDoubleClick, modify_ot_order_request.build())


def select_placed_order(base_request, act_ob, case_id, ord_id):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", ord_id])
    ob_ord_id = ExtractionDetail('orderBook.OrderId', 'Order ID')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_ord_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check placed order")
    verifier.compare_values('Order ID', ord_id, response[ob_ord_id.name])
    verifier.verify()


def check_order_book_after_amend(base_request, act_ob, case_id, ord_id, initial_qty):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Order ID", ord_id])
    ob_qty = ExtractionDetail('orderBook.Qty', 'Qty')
    ob_ord_id = ExtractionDetail('orderBook.OrderId', 'Order ID')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_ord_id,
                                                                                 ob_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('Order ID', ord_id, response[ob_ord_id.name])
    verifier.compare_values('New Qty not equal to initial', response[ob_qty.name].replace(',', ''), initial_qty,
                            verification_method=VerificationMethod.NOT_EQUALS)
    verifier.verify()


def place_esp_by_bid_btn(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.top_of_book(False)
    call(service.placeESPOrder, rfq_request.build())


def amend_order(base_request, service, qty):
    # order_details = FXOrderDetails()
    # order_details.set_qty(qty)
    # amend_order_request = ModifyFXOrderDetails(base_request)
    # amend_order_request.set_order_details(order_details)
    # call(ob_act.amendOrder, amend_order_request.build())
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())

def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_act = Stubs.win_act_order_book
    ar_service = Stubs.win_act_aggregated_rates_service
    fx_ob_service = Stubs.win_act_order_book_fx

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_data = BaseTileData(base=case_base_request)

    owner = 'QA5'
    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    initial_qty = str(random.randint(1000000, 5000000))
    new_qty = str(random.randint(1000000, int(initial_qty)))

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor, initial_qty)
        place_esp_by_bid_btn(case_base_request)
        pips = extract_price_from_ot(base_data, order_ticket_service)
        modify_order_ticket(case_base_request, order_ticket_service, pips[0], pips[1])
        placed_order_id = check_order_book(case_base_request, ob_act, case_id, tenor, owner, initial_qty)

        # Step 2
        open_order_ticket_via_double_click(fx_ob_service, case_base_request)
        amend_order(case_base_request, order_ticket_service, new_qty)

        # Step 3
        check_order_book_after_amend(case_base_request, ob_act, case_id, placed_order_id, initial_qty)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
