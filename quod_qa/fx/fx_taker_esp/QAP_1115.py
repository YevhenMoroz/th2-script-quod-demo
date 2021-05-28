import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide, \
    ContextActionRatesTile, ContextActionType
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import OrderTicketDetails, FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails, NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def place_order(base_request, service):
    rfq_request = PlaceESPOrder(details=base_request)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    call(service.placeESPOrder, rfq_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def get_my_orders_details(base_request, ob_act, case_id, owner):
    main_order_details = OrdersDetails()
    execution_id = bca.client_orderid(4)
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(execution_id)
    ob_owner = ExtractionDetail("myorderbook.owner", "Owner")
    ob_display_px = ExtractionDetail("myorderbook.px", "DisplayPx")
    main_order_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_owner,
                                                                                 ob_display_px])))
    response = call(ob_act.getMyOrdersDetails, main_order_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check My Order book")
    # verifier.compare_values("Display Px", display_px, response[ob_display_px])
    verifier.compare_values("Owner", owner, response[ob_owner.name])
    verifier.verify()


def check_order_book(base_request, act_ob, case_id, instr_type, owner):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
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

    owner = Stubs.custom_config['qf_trading_fe_user_309']

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    # TODO Extract data from Order Ticket

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, "EUR", "USD", "Spot")
        place_order(base_esp_details, ar_service)
        modify_order_ticket(case_base_request, order_ticket_service)
        # Step 2-3
        get_my_orders_details(case_base_request, ob_act, case_id, owner)
        # Step 4-5
        check_order_book(case_base_request, ob_act, case_id, "Spot", owner)

    except Exception:
        logging.error("Error execution", exc_info=True)
    # finally:
    #     try:
    #         # Close tile
    #         call(ar_service.closeESPTile, base_esp_details.build())
    #     except Exception:
    #         logging.error("Error execution", exc_info=True)
