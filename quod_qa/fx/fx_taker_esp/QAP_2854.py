import logging
from pathlib import Path

import timestring

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import m1_front_end
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, \
    ContextActionType, ExtractRatesTileDataRequest
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail

from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    modify_request.add_context_action(venue_filter)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def open_aggregated_rates(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    add_agr_rates = ContextActionRatesTile.add_aggregated_rates(details=base_request)
    modify_request.add_context_actions([add_agr_rates])
    call(service.modifyRatesTile, modify_request.build())


def check_qty_band(base_request, service, case_id, qty, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Qty", "Qty"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Qty", "Qty"))
    response = call(service.extractESPAggrRatesTableValues, extract_table_request.build())

    ask_qty = response["rateTileAsk.Qty"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Qty band")
    verifier.compare_values("Ask qty", qty, ask_qty)

    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "GBP"
    to_curr = "USD"
    tenor = "Spot"
    venue = "HSBC"

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor, venue)
        open_aggregated_rates(base_esp_details, ar_service)
        check_qty_band(base_esp_details, ar_service, case_id, "200K", 1)
        check_qty_band(base_esp_details, ar_service, case_id, "6M", 2)
        check_qty_band(base_esp_details, ar_service, case_id, "1.2B", 3)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
