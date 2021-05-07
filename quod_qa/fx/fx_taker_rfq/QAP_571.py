import logging
from pathlib import Path

from custom import basic_custom_actions as bca

from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues, ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_tile(base_request, service, **kwargs):
    modify_request = ModifyRFQTileRequest(details=base_request)
    if "qty" in kwargs.keys():
        modify_request.set_quantity(kwargs["qty"])
    if "qty_as_string" in kwargs.keys():
        modify_request.set_quantity_as_string(kwargs["qty_as_string"])
    if "from_c" in kwargs.keys():
        modify_request.set_from_currency(kwargs["from_c"])
    if "to_c" in kwargs.keys():
        modify_request.set_to_currency(kwargs["to_c"])

    call(service.modifyRFQTile, modify_request.build())


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


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_qty = 5000000
    case_default_currency = "AUD/BRL"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_cur_pair = case_from_currency + "/" + case_to_currency
    case_string_qty = "1m"
    case_string_qty_to_int = 1000000
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        check_currency_pair(base_rfq_details, ar_service, case_id, case_default_currency)
        # Step 2
        # TODO Change currency pair from drop down
        # Step 3
        modify_tile(base_rfq_details, ar_service, from_c=case_from_currency, to_c=case_to_currency)
        check_currency_pair(base_rfq_details, ar_service, case_id, case_cur_pair)
        # Step 4
        modify_tile(base_rfq_details, ar_service, qty=case_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_qty)
        # Step 5
        modify_tile(base_rfq_details, ar_service, qty_as_string=case_string_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_string_qty_to_int)
        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
