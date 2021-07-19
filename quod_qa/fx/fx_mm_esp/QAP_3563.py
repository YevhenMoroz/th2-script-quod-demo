import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues, \
    PlaceRatesTileOrderRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def check_ask_price(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = response["rates_tile.ask_large"]
    return ask


def place_order(base_request, service, client, slippage):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def check_order_book(base_request, act_ob, case_id, owner, client, price):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Owner", owner, "Client ID", client])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    exec_price = ExtractionDetail("executions.price", "ExecPrice")
    exec_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_detail=exec_price))
    exec_details = OrdersDetails.create(info=exec_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts]),
            sub_order_details=exec_details))

    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("InstrType", "Spot", response[ob_instr_type.name])
    verifier.compare_values("Sts", "Filled", response[ob_exec_sts.name])
    verifier.compare_values("ExecPrice", price, response[exec_price.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ob_act = Stubs.win_act_order_book

    instrument = "EUR/CAD-SPOT"
    client_tier = "Palladium"
    client = "Palladium1"
    owner = Stubs.custom_config['qf_trading_fe_user_309']

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        ask_price = check_ask_price(base_details, cp_service)
        # Step 2
        place_order(base_details, cp_service, client, "0")
        check_order_book(case_base_request, ob_act, case_id, owner, client, ask_price)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
