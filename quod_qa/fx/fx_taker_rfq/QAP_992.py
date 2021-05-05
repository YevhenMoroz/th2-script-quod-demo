import logging
from pathlib import Path
import timestring
import rule_management as rm
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import ndf_m1_front_end, ndf_spo_front_end, fixing_ndf_m1_front_end, \
    ndf_m2_front_end, fixing_ndf_m2_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, cur1, cur2, near_tenor):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(near_tenor)
    call(service.modifyRFQTile, modify_request.build())


def change_tenor(base_request, service, tenor):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_near_tenor(tenor)
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


def check_fixing_date(base_request, service, case_id, date):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.extract_near_maturity_date("aggrRfqTile.nearFixingDate")
    extract_value.set_extraction_id(extraction_id)
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_date = response["aggrRfqTile.nearFixingDate"]
    extract_date = timestring.Date(extract_date)
    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Fixing date on RFQ tile")
    verifier.compare_values("Date", date, str(extract_date))
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    case_name = Path(__file__).name[:-3]
    case_from_currency = "USD"
    case_to_currency = "PHP"
    case_near_tenor = "Spot"
    case_tenor_1m = "1M"
    case_tenor_2m = "2M"
    ndf_date_spot = ndf_spo_front_end()
    ndf_date_1m = ndf_m1_front_end()
    fixing_ndf_date_1m = fixing_ndf_m1_front_end()
    ndf_date_2m = ndf_m2_front_end()
    fixing_ndf_date_2m = fixing_ndf_m2_front_end()

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
        modify_rfq_tile(base_rfq_details, ar_service, case_from_currency, case_to_currency, case_near_tenor)
        check_date(base_rfq_details, ar_service, case_id, ndf_date_spot)
        # Step 2
        change_tenor(base_rfq_details, ar_service, case_tenor_1m)
        check_date(base_rfq_details, ar_service, case_id, ndf_date_1m)
        # Step 3
        check_fixing_date(base_rfq_details, ar_service, case_id, fixing_ndf_date_1m)
        # Step 4
        change_tenor(base_rfq_details, ar_service, case_tenor_2m)
        check_date(base_rfq_details, ar_service, case_id, ndf_date_2m)
        check_fixing_date(base_rfq_details, ar_service, case_id, fixing_ndf_date_2m)
        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)
