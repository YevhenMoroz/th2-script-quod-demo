import logging
from pathlib import Path

from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from custom import basic_custom_actions as bca
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile(base_request, service, far_tenor):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_far_leg_tenor(far_tenor)
    call(service.modifyRFQTile, modify_request.build())


def change_far_leg_qty(base_request, service, qty):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_far_leg_quantity_as_string(qty)
    call(service.modifyRFQTile, modify_request.build())


def check_qty(base_request, service, case_id, far_qty):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_far_leg_qty("aggrRfqTile.farqty")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_far_qty = response["aggrRfqTile.farqty"].replace(',', '')

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Qty in RFQ tile")
    verifier.compare_values('Far leg qty', str(far_qty), extract_far_qty[:-3])
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_far_tenor = "1W"
    case_1k_qty = "1k"
    case_1m_qty = '1m'
    case_1b_qty = "1b"
    case_1kk_qty = "1kk"

    case_expected_1k = 1000
    case_expected_1m = 1000000
    case_expected_1b = 1000000000

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
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
        modify_rfq_tile(base_rfq_details, ar_service, case_far_tenor)
        # Step 2
        change_far_leg_qty(base_rfq_details, ar_service, case_1m_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_expected_1m)
        # Step 3
        change_far_leg_qty(base_rfq_details, ar_service, case_1k_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_expected_1k)
        # Step 4
        change_far_leg_qty(base_rfq_details, ar_service, case_1b_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_expected_1b)
        # Step 5
        change_far_leg_qty(base_rfq_details, ar_service, case_1kk_qty)
        check_qty(base_rfq_details, ar_service, case_id, case_expected_1k)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
