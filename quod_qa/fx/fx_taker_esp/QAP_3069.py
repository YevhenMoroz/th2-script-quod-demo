import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide, \
    ContextActionRatesTile, ActionsRatesTile
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import DefaultFXValues, OptionOrderTicketRequest, \
    CustomCurrencySlippage
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def set_order_ticket_options(base_request, service, algo, strategy, child_strategy):
    order_ticket_options = OptionOrderTicketRequest(base=base_request)
    fx_values = DefaultFXValues([])
    fx_values.AggressiveStrategyType = algo
    fx_values.AggressiveStrategy = strategy
    fx_values.AggressiveChildStrategy = child_strategy
    order_ticket_options.set_default_fx_values(fx_values)
    call(service.setOptionOrderTicket, order_ticket_options.build())


def check_passive_strategy(base_request, service, case_id, algo, strategy, child_strategy):
    extract_value = ExtractFxOrderTicketValuesRequest(base_request)
    extract_value.get_strategy("orderTicket.strategy")
    extract_value.get_child_strategy("orderTicket.childStrategy")
    extract_value.get_algo("orderTicket.algo")

    response = call(service.extractFxOrderTicketValues, extract_value.build())

    extracted_algo = response["orderTicket.algo"]
    extracted_strategy = response["orderTicket.strategy"]
    extracted_child_strategy = response["orderTicket.childStrategy"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check order ticket Algo strategy")
    verifier.compare_values("Algo name", algo, extracted_algo)
    verifier.compare_values("Strategy name", strategy, extracted_strategy)
    verifier.compare_values("Child strategy name", child_strategy, extracted_child_strategy)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
    option_service = Stubs.win_act_options
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    curr_eur = "EUR"
    curr_usd = "USD"
    tenor = "Spot"
    algo = "Quod TWAP"
    strategy = "308TWAP"
    child_strategy = "Hedging_Test"

    try:
        # Step 1
        set_order_ticket_options(case_base_request, option_service, algo, strategy, child_strategy)
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, curr_eur, curr_usd, tenor)
        # Step 2
        place_order(base_esp_details, ar_service)
        check_passive_strategy(base_tile_data, order_ticket_service, case_id, algo, strategy, child_strategy)
        close_order_ticket(case_base_request, order_ticket_service)

        # Set settings back
        set_order_ticket_options(case_base_request, option_service, "Quod MultiListing", "Hedging_Test", "Hedging_Test")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
