import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide, \
    ExtractRatesTileDataRequest, ContextActionRatesTile, ActionsRatesTile
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, qty):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    new_order_details = NewFxOrderDetails()
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    call(service.placeFxOrder, new_order_details.build())


def click_one_click_button(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_click_on_one_click_button()
    call(service.modifyRatesTile, modify_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def open_direct_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    add_dve_action = ContextActionRatesTile.open_direct_venue_panel()
    modify_request.add_context_actions([venue_filter, add_dve_action])
    call(service.modifyRatesTile, modify_request.build())


def click_on_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    click_to_venue = ActionsRatesTile.click_to_ask_esp_order(venue)
    modify_request.add_action(click_to_venue)
    call(service.modifyRatesTile, modify_request.build())


def check_order_book(base_request, act_ob, case_id, instr_type, owner):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_display_px = ExtractionDetail("orderbook.displayPx", "DisplayPx")
    ob_owner = ExtractionDetail("orderbook.owner", "Owner")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_display_px,
                                                                                 ob_owner])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values("Owner", owner, response[ob_owner.name])
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_act = Stubs.win_act_order_book

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    owner = Stubs.custom_config['qf_trading_fe_user_309']
    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    venue = "CIT"
    qty = "5000000"

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        click_one_click_button(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        open_direct_venue(base_esp_details, ar_service, venue)
        click_on_venue(base_esp_details, ar_service, venue)
        check_order_book(case_base_request, ob_act, case_id, tenor, owner)
        # Step 2
        click_one_click_button(base_esp_details, ar_service)
        click_on_venue(base_esp_details, ar_service, venue)
        modify_order_ticket(case_base_request, order_ticket_service, qty)
        check_order_book(case_base_request, ob_act, case_id, tenor, owner)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
