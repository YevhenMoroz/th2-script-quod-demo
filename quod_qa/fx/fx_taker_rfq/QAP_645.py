import logging
from pathlib import Path
import timestring
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end, wk1_front_end, wk2_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, \
    ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_tile(base_request, service, **kwargs):
    modify_request = ModifyRFQTileRequest(details=base_request)
    if "qty" in kwargs.keys():
        modify_request.set_quantity_as_string(kwargs["qty"])
    if "change_c" in kwargs.keys():
        modify_request.set_change_currency(kwargs["change_c"])
    if "from_c" in kwargs.keys():
        modify_request.set_from_currency(kwargs["from_c"])
    if "to_c" in kwargs.keys():
        modify_request.set_to_currency(kwargs["to_c"])
    if "near_tenor" in kwargs.keys():
        modify_request.set_near_tenor(kwargs["near_tenor"])
    if "far_tenor" in kwargs.keys():
        modify_request.set_far_leg_tenor(kwargs["far_tenor"])

    call(service.modifyRFQTile, modify_request.build())


def check_qty(base_request, service, case_id, near_qty):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_quantity("aggrRfqTile.nearqty")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_near_qty = response["aggrRfqTile.nearqty"].replace(',', '')

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Qty in RFQ tile")
    verifier.compare_values('Near leg qty', str(near_qty), extract_near_qty[:-3])
    verifier.verify()


def check_date(base_request, service, case_id, near_date, far_date, flag):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    if flag is True:
        extract_value.extract_near_settlement_date("aggrRfqTile.nearSettlement")
    else:
        extract_value.extract_near_settlement_date("aggrRfqTile.nearSettlement")
        extract_value.extract_far_leg_settlement_date("aggrRfqTile.farSettlement")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_near_date = response["aggrRfqTile.nearSettlement"]
    extract_near_date = timestring.Date(extract_near_date)
    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Tenor date on RFQ tile")
    if flag is True:
        verifier.compare_values("Near settlement date", near_date, str(extract_near_date))
    else:
        extract_far_date = response["aggrRfqTile.farSettlement"]
        extract_far_date = timestring.Date(extract_far_date)
        verifier.compare_values("Near settlement date", near_date, str(extract_near_date))
        verifier.compare_values("Far settlement date", far_date, str(extract_far_date))
    verifier.verify()


def check_currency(base_request, service, case_id, currency):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_currency("aggrRfqTile.currency")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_currency = response["aggrRfqTile.currency"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check currency on RFQ tile")
    verifier.compare_values("Currency", currency, extract_currency)
    verifier.verify()


def check_currency_pair(base_request, service, case_id, currency_pair):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_currency_pair("aggrRfqTile.currencypair")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_currency_pair = response["aggrRfqTile.currencypair"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check currency pair on RFQ tile")
    verifier.compare_values("Currency", currency_pair, extract_currency_pair)
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_tenor_spot = "Spot"
    case_tenor_1w = "1W"
    case_tenor_2w = "2W"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_cur_pair = case_from_currency + "/" + case_to_currency
    spot = spo_front_end()
    wk1 = wk1_front_end()
    wk2 = wk2_front_end()
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        # Step 2
        modify_tile(base_rfq_details, ar_service, near_tenor=case_tenor_spot, from_c=case_from_currency,
                    to_c=case_to_currency)
        check_currency_pair(base_rfq_details, ar_service, case_id, case_cur_pair)
        # Step 3
        check_date(base_rfq_details, ar_service, case_id, spot, wk1, True)
        # Step 4
        modify_tile(base_rfq_details, ar_service, near_tenor=case_tenor_1w)
        check_date(base_rfq_details, ar_service, case_id, wk1, wk1, True)
        # Step 5
        modify_tile(base_rfq_details, ar_service, far_tenor=case_tenor_2w)
        check_date(base_rfq_details, ar_service, case_id, wk1, wk2, False)
        # Step 6
        modify_tile(base_rfq_details, ar_service, change_c=True)
        check_currency(base_rfq_details, ar_service, case_id, case_to_currency)
        # Step 7
        modify_tile(base_rfq_details, ar_service, qty='1k')
        check_qty(base_rfq_details, ar_service, case_id, "1000")
        # Step 8
        modify_tile(base_rfq_details, ar_service, qty='1m')
        check_qty(base_rfq_details, ar_service, case_id, "1000000")
        # Step 9
        modify_tile(base_rfq_details, ar_service, near_tenor=case_tenor_spot)
        check_date(base_rfq_details, ar_service, case_id, spot, wk1, True)
        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
