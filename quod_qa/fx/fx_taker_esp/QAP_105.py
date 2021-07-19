import logging
from pathlib import Path

import timestring

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import m1_front_end, spo_front_end, wk1_front_end, y1_front_end, wk3_front_end
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, \
     ExtractRatesTileDataRequest
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail

from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from datetime import datetime, timedelta

def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):

    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def check_esp_tile(base_request, service, case_id, instrument, date):

    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_instrument("ratesTile.instrument")
    extraction_value.extract_tenor("ratesTile.date")

    response = call(service.extractRatesTileValues, extraction_value.build())

    extracted_instrument = response["ratesTile.instrument"]
    extracted_tenor_date = response["ratesTile.date"]
    extracted_tenor_date = timestring.Date(extracted_tenor_date)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value in ESP tile")
    verifier.compare_values("Instrument ", instrument, extracted_instrument)
    verifier.compare_values("Date ", date, str(extracted_tenor_date))
    verifier.verify()


def execute(report_id, session_id):
    start = datetime.now()
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id=session_id, event_id=case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    # Instrument setup
    from_curr = "EUR"
    to_curr = "USD"

    # Tenors front end
    spot = spo_front_end()
    wk1 = wk1_front_end()
    wk3 = wk3_front_end()
    m1 = m1_front_end()
    y1 = y1_front_end()

    tenors_dict = {
        'Spot': spot,
        '1W': wk1,
        '3W': wk3,
        '1M': m1,
        '1Y': y1
    }

    try:

        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)

        # Step 2-6 Checking data format for tenors

        for tenor, tenor_front_end in tenors_dict.items():
            instrument = from_curr + "/" + to_curr + "-" + tenor
            modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
            check_esp_tile(base_esp_details, ar_service, case_id, instrument, tenor_front_end)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            print(f'{case_name} duration time = ' + str(datetime.now() - start))
            call(ar_service.closeRatesTile, base_esp_details.build())
            # call(ar_service.closeWindow, case_base_request)
        except Exception:
            logging.error("Error execution", exc_info=True)
