import logging
from pathlib import Path
import timestring
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import ndf_wk1_front_end, ndf_m1_front_end, ndf_y1_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ExtractRatesTileDataRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def chek_date(base_request, service, case_id, date):
    extract_value = ExtractRatesTileDataRequest(base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_tenor_date("ratesTile.TenorDate")
    response = call(service.extractRatesTileValues, extract_value.build())

    extracted_date = response["ratesTile.TenorDate"]
    extracted_date = timestring.Date(extracted_date)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check date")
    verifier.compare_values("Date", date, str(extracted_date))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    from_curr = "USD"
    to_curr = "PHP"

    tenor_1w = "1W"
    tenor_1m = "1M"
    tenor_1y = "1Y"
    wk1 = ndf_wk1_front_end()
    m1 = ndf_m1_front_end()
    y1 = ndf_y1_front_end()

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_1w)
        chek_date(base_esp_details, ar_service, case_id, wk1)
        # Step 2
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_1m)
        chek_date(base_esp_details, ar_service, case_id, m1)
        # Step 3
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor_1y)
        chek_date(base_esp_details, ar_service, case_id, y1)


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
