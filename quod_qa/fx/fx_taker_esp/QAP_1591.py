import logging
from pathlib import Path

import timestring

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import m1_front_end
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, \
    ExtractRatesTileDataRequest
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail

from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def open_aggregated_rates(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    add_agr_rates = ContextActionRatesTile.add_aggregated_rates(details=base_request)
    modify_request.add_context_actions([add_agr_rates])
    call(service.modifyRatesTile, modify_request.build())


def check_esp_tile(base_request, service, case_id, instrument, date):
    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_instrument("ratesTile.instrument")
    extraction_value.extract_tenor_date("ratesTile.date")
    response = call(service.extractRatesTileValues, extraction_value.build())
    extracted_instrument = response["ratesTile.instrument"]
    extracted_tenor_date = response["ratesTile.date"]
    extracted_tenor_date = timestring.Date(extracted_tenor_date)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value in ESP tile")
    verifier.compare_values("Instrument ", instrument, extracted_instrument)
    verifier.compare_values("Date ", date, str(extracted_tenor_date))
    verifier.verify()


def check_aggregated_rates(base_request, service, case_id):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Pts", "Pts"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Pts", "Pts"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Px", "Px"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Px", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Spot", "Spot"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Spot", "Spot"))
    response = call(service.extractESPAggrRatesTableValues, extract_table_request.build())

    ask_pts = response["rateTileAsk.Pts"]
    bid_pts = response["rateTileBid.Pts"]
    ask_px = response["rateTileAsk.Px"]
    bid_px = response["rateTileBid.Px"]
    ask_spot = response["rateTileAsk.Spot"]
    bid_spot = response["rateTileBid.Spot"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check pts")
    verifier.compare_values("Ask pts", "", ask_pts, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Bid pts", "", bid_pts, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Ask px", "", ask_px, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Bid px", "", bid_px, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Ask spot", "", ask_spot, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Bid spot", "", bid_spot, VerificationMethod.NOT_EQUALS)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "1M"
    m1 = m1_front_end()
    instrument = from_curr + "/" + to_curr + "-" + tenor

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        # Step 2
        check_esp_tile(base_esp_details, ar_service, case_id, instrument, m1)
        # Step 3
        open_aggregated_rates(base_esp_details, ar_service)
        check_aggregated_rates(base_esp_details, ar_service, case_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
