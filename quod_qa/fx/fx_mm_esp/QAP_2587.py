import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileTableValuesRequest, \
    ExtractRatesTileValues
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


def extract_ask_value(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    return ask


def extract_column_spot(base_request, service):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askSpot", "Spot"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidSpot", "Spot"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    return response["rateTile.askSpot"]


def check_spot(case_id, spot, spot_1w):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare spot")
    verifier.compare_values("Value of spot", str(spot), spot_1w)
    verifier.verify()


def check_pts_column(base_request, service, case_id, px, spot):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askPts", "Pts"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidPts", "Pts"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    extracted_pts = response["rateTile.askPts"]
    calculated_pts = round(((float(px) - float(spot)) * 10000), 3)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check calculation of pts")
    verifier.compare_values("Pts", str(calculated_pts), extracted_pts[:-2])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    instrument_1w = "EUR/USD-1W"
    instrument_spo = "EUR/USD-SPOT"
    client_tier = "Silver"

    case_base_request = get_base_request(session_id, case_id)
    base_details_spo = BaseTileDetails(base=case_base_request, window_index=0)
    base_details_1w = BaseTileDetails(base=case_base_request, window_index=1)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details_spo, cp_service)
        create_or_get_rates_tile(base_details_1w, cp_service)
        modify_rates_tile(base_details_spo, cp_service, instrument_spo, client_tier)
        modify_rates_tile(base_details_1w, cp_service, instrument_1w, client_tier)
        # Step 2
        spot = extract_ask_value(base_details_spo, cp_service)
        column_spot = extract_column_spot(base_details_1w, cp_service)
        check_spot(case_id, spot, column_spot)

        ask_1w = extract_ask_value(base_details_1w, cp_service)
        check_pts_column(base_details_1w, cp_service, case_id, ask_1w, column_spot)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details_spo.build())
            call(cp_service.closeRatesTile, base_details_1w.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
