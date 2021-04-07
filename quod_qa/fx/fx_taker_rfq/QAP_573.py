import logging
import time

import timestring

import rule_management as rm
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, tom, wk1, wk1_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


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


def modify_order(base_request, service, cur1, cur2, client, tenor):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def execute(report_id):
    common_act = Stubs.win_act
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    case_name = "QAP-573"
    quote_owner = "QA2"
    case_client = "MMCLIENT2"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_tenor = "1W"
    date = wk1_front_end()

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
        modify_order(base_rfq_details, ar_service, case_from_currency,
                     case_to_currency, case_client, case_tenor)
        check_date("RFQ", base_rfq_details, ar_service, case_id, date)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)
