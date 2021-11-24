import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import FXConfigsRequest, DefaultFXValues, OptionOrderTicketRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def send_order(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def set_order_ticket_options(base_request, service, client):
    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    fx_values = DefaultFXValues([])
    fx_values.Client = client
    order_ticket_options.set_default_fx_values(fx_values)
    call(service.setOptionOrderTicket, order_ticket_options.build())


def check_client_in_ord_t(base_request, service, case_id, client):
    extract_value = ExtractFxOrderTicketValuesRequest(base_request)
    extract_value.get_client("orderTicket.Client")
    response = call(service.extractFxOrderTicketValues, extract_value.build())

    extracted_client = response["orderTicket.Client"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check client in order ticket")
    verifier.compare_values("Client", client, extracted_client)
    verifier.verify()


def check_order_book(base_request, act_ob, case_id, owner, client):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner])
    ob_client = ExtractionDetail("orderBook.client", "Client Name")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_client])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Client", client, response[ob_client.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
    option_service = Stubs.win_act_options
    ob_service = Stubs.win_act_order_book
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"

    client = "ASPECT_CITI"
    owner = Stubs.custom_config['qf_trading_fe_user']

    try:
        # Step 1-2
        set_order_ticket_options(case_base_request, option_service, client)
        # Step 3
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        # Step 4
        place_order(base_esp_details, ar_service)
        check_client_in_ord_t(base_tile_data, order_ticket_service, case_id, client)
        # Step 5
        send_order(case_base_request, order_ticket_service)
        check_order_book(case_base_request, ob_service, case_id, owner, client)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
