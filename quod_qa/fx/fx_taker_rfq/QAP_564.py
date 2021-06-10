import logging
from pathlib import Path

import timestring
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1_front_end, spo_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile(base_request, service, near_qty, cur1, cur2, near_tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_date(base_request, service, case_id, date):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.extract_near_settlement_date("aggrRfqTile.nearSettlement")
    extract_value.set_extraction_id(extraction_id)
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_date = response["aggrRfqTile.nearSettlement"]
    extract_date = timestring.Date(extract_date)
    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Tenor date on RFQ tile")
    verifier.compare_values("Date", date, str(extract_date))
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


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(base_rfq_details)

    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "ASPECT_CITI"
    case_pair = case_from_currency + "/" + case_to_currency
    case_qty = 10000000
    case_qty2 = "1m"
    case_qty_1m = "1000000"
    case_qty3 = "100k"
    case_qty_100kk = "100000"
    case_tenor1 = "Spot"
    case_tenor2 = "1W"
    spo_front_end()
    wk1_front_end()

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)

        # Step 2
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_tenor1, case_client)
        check_currency_pair(base_rfq_details, ar_service, case_id, case_pair)

        # Step 3
        check_date(base_rfq_details, ar_service, case_id, spo_front_end())

        # Step 4
        modify_request.set_change_currency(True)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_currency(base_rfq_details, ar_service, case_id, case_to_currency)

        # Step 5
        modify_request.set_quantity_as_string(case_qty2)
        modify_request.set_change_currency(False)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty(base_rfq_details, ar_service, case_id, case_qty_1m)

        # Step 6
        modify_request.set_quantity_as_string(case_qty3)
        modify_request.set_change_currency(False)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty(base_rfq_details, ar_service, case_id, case_qty_100kk)

        # Step 7
        modify_request.set_near_tenor(case_tenor2)
        modify_request.set_change_currency(False)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_date(base_rfq_details, ar_service, case_id, wk1_front_end())
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
