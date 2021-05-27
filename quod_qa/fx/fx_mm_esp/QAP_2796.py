import logging
from datetime import datetime
from pathlib import Path

import timestring

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def check_date(base_request, service, case_id, expected_date):
    extract_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_request.set_extraction_id(extraction_id)
    extract_request.extract_value_date("ratesTile.Date")
    response = call(service.extractRateTileValues, extract_request.build())

    now = datetime.now()
    extracted_value = response["ratesTile.Date"]
    date = extracted_value + "-" + str(now.year)
    extracted_date = datetime.strptime(date, "%d-%B-%Y").strftime('%Y-%m-%d %H:%M:%S')

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Tenor date on pricing tile")
    verifier.compare_values("Date", expected_date, str(extracted_date))
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "NOK/SEK-Spot"
    client_tier = "Silver"
    date_spo = spo_front_end()

    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        # Step 2
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        check_date(base_details, cp_service, case_id, date_spo)


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
