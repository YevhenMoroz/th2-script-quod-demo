import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileTableValuesRequest, \
    DeselectRowsRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def switch_to_tired(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.toggle_tiered()
    call(service.modifyRatesTile, modify_request.build())


def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())


def press_executable(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_executable()
    call(service.modifyRatesTile, modify_request.build())


def check_tile_value(base_request, service, case_id, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_ask_extraction_fields([ExtractionDetail("rateTile.askPx", "Px"),
                                                     ExtractionDetail("rateTile.askPub", "Pub")])
    extract_table_request.set_bid_extraction_fields([ExtractionDetail("rateTile.bidPx", "Px"),
                                                     ExtractionDetail("rateTile.bidPub", "Pub")])
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value in columns")
    verifier.compare_values("Ask Px", "", response["rateTile.askPx"])
    verifier.compare_values("Bid Px", "", response["rateTile.bidPx"])
    verifier.compare_values("Ask Pub", "", response["rateTile.askPub"])
    verifier.compare_values("Bid Pub", "", response["rateTile.bidPub"])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    instrument = "EUR/USD-SPOT"
    client_tier = "Silver"

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        switch_to_tired(base_details, cp_service)
        # Step 2
        press_executable(base_details, cp_service)

        check_tile_value(base_details, cp_service, case_id, 1)
        check_tile_value(base_details, cp_service, case_id, 2)
        check_tile_value(base_details, cp_service, case_id, 3)
        request = DeselectRowsRequest(base_details)
        call(cp_service.deselectRows, request.build())
        # Step 3
        press_executable(base_details, cp_service)
        press_pricing(base_details, cp_service)

        check_tile_value(base_details, cp_service, case_id, 1)
        check_tile_value(base_details, cp_service, case_id, 2)
        check_tile_value(base_details, cp_service, case_id, 3)
        request = DeselectRowsRequest(base_details)
        call(cp_service.deselectRows, request.build())
        press_pricing(base_details, cp_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
