import logging
from datetime import datetime
from pathlib import Path
import timestring
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import next_working_day_after_25dec_front_end, next_monday_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, date, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_settlement_date(bca.get_t_plus_date(date, is_weekend_holiday=False))
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_date(exec_id, base_request, service, case_id, date):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.extract_near_settlement_date("aggrRfqTile.nearSettlement")
    extract_value.set_extraction_id(exec_id)
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_date = response["aggrRfqTile.nearSettlement"]
    extract_date = timestring.Date(extract_date)
    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Tenor date on RFQ tile")
    verifier.compare_values("Date", date, str(extract_date))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_qty = 1000000
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "ASPECT_CITI"
    click_to_25dec = int(str(datetime(2021, 12, 25) - datetime.now()).split()[0])
    click_to_sunday = 7 - int(datetime.now().strftime('%w'))
    next_monday_front_end()
    next_working_day_after_25dec_front_end()

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(base_rfq_details)

    try:
        
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, click_to_sunday, case_client)
        check_date("RFQ", base_rfq_details, ar_service, case_id, next_monday_front_end())

        # Step 2
        modify_request.set_settlement_date(bca.get_t_plus_date(click_to_25dec, is_weekend_holiday=False))
        call(ar_service.modifyRFQTile, modify_request.build())
        check_date("RFQ", base_rfq_details, ar_service, case_id, next_working_day_after_25dec_front_end())

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
