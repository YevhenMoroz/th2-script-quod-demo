import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileTableValuesRequest
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


def check_band_column(base_request, service, case_id, row, value):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBand", "Band"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBand", "Band"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check rounding values")
    verifier.compare_values("Ask band", value, response["rateTile.askBand"])
    verifier.compare_values("Bid band", value, response["rateTile.bidBand"])
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    instrument = "GBP/USD-SPOT"
    client_tier = "Palladium"
    value_200k = "200K"
    value_6m = "6M"
    value_1_2b = "1.2B"
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
        check_band_column(base_details, cp_service, case_id, 1, value_200k)
        check_band_column(base_details, cp_service, case_id, 2, value_6m)
        check_band_column(base_details, cp_service, case_id, 3, value_1_2b)


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)