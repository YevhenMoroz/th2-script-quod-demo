import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest
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


def place_order(base_request, service, client, slippage, qty):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.set_quantity(qty)
    place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def check_order_book(base_request, act_ob, instr_type, case_id, qty, owner, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Owner", owner, "Client ID", client])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.compare_values("Qty", qty, response[ob_qty.name].replace(',', ''))
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-SPOT"
    client_tier = "Gold_Night"
    client = "CLIENT2"
    slippage = "1"
    instrument_type = "Spot"
    qty = "1000000"
    owner = "ostronov"

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:

        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        place_order(base_details, cp_service, client, slippage, qty)
        check_order_book(case_base_request, ob_service, instrument_type, case_id,
                         qty, owner, client)
    # TODO place order by double click on row
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # Close tile
        call(cp_service.closeWindow, case_base_request)
