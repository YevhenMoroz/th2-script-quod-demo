import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails
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


def modify_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_pending(True)
    order_ticket.set_place(True)
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def check_order_book(base_request, act_ob, case_id, owner, status, *args):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner])
    ob_status = ExtractionDetail("orderBook.Status", "Sts")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_status])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    method = ""
    if "EQUAL" in args:
        method = VerificationMethod.EQUALS
    if "NOT_EQUAL" in args:
        method = VerificationMethod.NOT_EQUALS
    verifier.set_event_name("Check Order book")
    verifier.compare_values("InstrType", status, response[ob_status.name], method)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
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
    equal = "EQUAL"
    not_equal = "NOT_EQUAL"

    owner = Stubs.custom_config['qf_trading_fe_user_309']
    sts_validated = "Validated"

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
        modify_order_ticket(case_base_request, order_ticket_service)
        check_order_book(case_base_request, ob_service, case_id, owner, sts_validated, equal)
        # Step 3
        # TODO Amend the order
        # Step 4
        # TODO Change qty or price
        # Step 5
        # TODO Release order

    except Exception:
        logging.error("Error execution", exc_info=True)
    # finally:
    #     try:
    #         # Close tile
    #         call(ar_service.closeRatesTile, base_esp_details.build())
    #     except Exception:
    #         logging.error("Error execution", exc_info=True)
