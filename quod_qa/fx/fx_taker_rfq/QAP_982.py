import logging
from pathlib import Path
import timestring
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def check_default_value_rfq_tile(exec_id, base_request, service, case_id, curr_pair, qty, near_tenor, date,
                                 curr_button):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_tenor("aggrRfqTile.nearTenor")
    extract_value.extract_near_settlement_date("aggrRfqTile.nearSettlement")
    extract_value.extract_quantity("aggrRfqTile.qty")
    extract_value.extract_currency_pair("aggrRfqTile.currPair")
    extract_value.extract_currency("aggrRfqTile.curr")
    response = call(service.extractRFQTileValues, extract_value.build())

    extract_tenor = response["aggrRfqTile.nearTenor"]
    extract_near_setl_date = response["aggrRfqTile.nearSettlement"]
    extract_near_setl_date = timestring.Date(extract_near_setl_date)
    extract_qty = response["aggrRfqTile.qty"]
    extract_cur_pair = response["aggrRfqTile.currPair"]
    extract_cur = response["aggrRfqTile.curr"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify default value in RFQ tile")
    verifier.compare_values("Tenor", near_tenor, extract_tenor)
    verifier.compare_values("Near Setll Date", date, str(extract_near_setl_date))
    verifier.compare_values("Qty", qty, extract_qty)
    verifier.compare_values("Currencies pair", curr_pair, extract_cur_pair)
    verifier.compare_values("Currencies button", curr_button, extract_cur)
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]

    case_cur_pair = "AUD/BRL"
    case_qty = "10,000,000.00"
    case_near_tenor = "Spot"
    case_date = spo_front_end()
    case_curr_button = "AUD"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        create_or_get_rfq(base_rfq_details, ar_service)
        check_default_value_rfq_tile("CDV_0", base_rfq_details, ar_service, case_id, case_cur_pair,
                                     case_qty, case_near_tenor, case_date, case_curr_button)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
