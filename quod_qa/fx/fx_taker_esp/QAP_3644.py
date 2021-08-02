import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import FXConfigsRequest, DefaultFXValues, OptionOrderTicketRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def set_one_click_mode(base_request, service, mode):
    fx_configs = FXConfigsRequest(base=base_request)
    fx_configs.set_one_click_mode(mode)
    call(service.setOptionForexConfigs, fx_configs.build())


def click_one_click_button(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_click_on_one_click_button()
    call(service.modifyRatesTile, modify_request.build())


def set_order_ticket_options(base_request, service, ord_type, tif, agr_str_t, str_t, client):
    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    fx_values = DefaultFXValues([])
    fx_values.AggressiveTIF = tif
    fx_values.AggressiveOrderType = ord_type
    fx_values.AggressiveStrategyType = agr_str_t
    fx_values.AggressiveStrategy = str_t
    fx_values.Client = client
    order_ticket_options.set_default_fx_values(fx_values)
    call(service.setOptionOrderTicket, order_ticket_options.build())


def check_order_book(base_request, act_ob, case_id, strategy, owner, ord_type, tif, client):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner])
    ob_strategy = ExtractionDetail("orderBook.strategy", "Strategy")
    ob_type = ExtractionDetail("orderBook.type", "OrdType")
    ob_tif = ExtractionDetail("orderBook.tif", "TIF")
    ob_client = ExtractionDetail("orderBook.client", "Client Name")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_strategy,
                                                                                 ob_type,
                                                                                 ob_tif,
                                                                                 ob_client])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("InstrType", strategy, response[ob_strategy.name])
    verifier.compare_values("Order Type", ord_type, response[ob_type.name])
    verifier.compare_values("Order TIF", tif, response[ob_tif.name])
    verifier.compare_values("Client", client, response[ob_client.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    option_service = Stubs.win_act_options
    ob_service = Stubs.win_act_order_book
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"

    tif = "FillOrKill"
    order_type = "Limit"
    agr_str_t = "Quod MultiListing"
    agr_str = "Hedging_Test"
    client = "ASPECT_CITI"
    owner = Stubs.custom_config['qf_trading_fe_user']

    single_click = "SingleClick"

    try:
        # Step 1
        set_order_ticket_options(case_base_request, option_service, order_type, tif,
                                 agr_str_t, agr_str, client)
        set_one_click_mode(case_base_request, option_service, single_click)
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        # Step 2
        click_one_click_button(base_esp_details, ar_service)
        place_order(base_esp_details, ar_service)
        check_order_book(case_base_request, ob_service, case_id, agr_str, owner,
                         order_type, tif, client)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
