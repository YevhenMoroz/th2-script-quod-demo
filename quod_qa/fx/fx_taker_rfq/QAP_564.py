import logging

import timestring

import rule_management as rm
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, wk1, wk1_front_end, spo_front_end
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent


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


def check_qty(exec_id, base_request, service, case_id, near_qty):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_quantity("aggrRfqTile.nearqty")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_near_qty = response["aggrRfqTile.nearqty"].replace(',', '')

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Qty in RFQ tile")
    verifier.compare_values('Near leg qty', str(near_qty), extract_near_qty[:-3])
    verifier.verify()


def check_currency(exec_id, base_request, service, case_id, currency):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_currency("aggrRfqTile.currency")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_currency = response["aggrRfqTile.currency"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check currency on RFQ tile")
    verifier.compare_values("Currency", currency, extract_currency)


def check_currency_pair(exec_id, base_request, service, case_id, currency_pair):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_currency_pair("aggrRfqTile.currency")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_currency_pair = response["aggrRfqTile.currencypair"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check currency on RFQ tile")
    verifier.compare_values("Currency", currency_pair, extract_currency_pair)


def execute(report_id):
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    # print_active_rules()
    case_name = "QAP-564"
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(base_rfq_details)

    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "MMCLIENT2"
    case_pair = case_from_currency + "/" + case_to_currency
    case_qty = 10000000
    # TODO Wait to change type for qty field
    case_qty2 = 1000000
    case_qty3 = 100000
    case_tenor1 = "Spot"
    case_tenor2 = "1W"
    spo_front_end()
    wk1_front_end()

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)

        # Step 2
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_tenor1, case_client)
        check_currency_pair("RFQ_0", base_rfq_details, ar_service, case_id, case_pair)

        # Step 3
        check_date("RFQ_1", base_rfq_details, ar_service, case_id, spo_front_end())

        # Step 4
        modify_request.set_change_currency()
        call(ar_service.modifyRFQTile, modify_request.build())
        check_currency("RFQ_2", base_rfq_details, ar_service, case_id, case_to_currency)

        # Step 5
        modify_request.set_quantity(case_qty2)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ_3", base_rfq_details, ar_service, case_id, case_qty2)

        # Step 6
        modify_request.set_quantity(case_qty3)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ_3", base_rfq_details, ar_service, case_id, case_qty3)

        # Step 7
        modify_request.set_near_tenor(case_tenor2)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_date("RFQ_1", base_rfq_details, ar_service, case_id, wk1_front_end())

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)
