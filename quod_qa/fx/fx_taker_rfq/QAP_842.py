import logging
import time
from pathlib import Path

import rule_management as rm
from custom import basic_custom_actions as bca

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


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_qty(base_request, service, case_id, near_qty):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_quantity("aggrRfqTile.nearqty")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_near_qty = response["aggrRfqTile.nearqty"].replace(',', '')
    print(response)

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Qty in RFQ tile")
    verifier.compare_values('Near leg qty', str(near_qty), extract_near_qty[:-3])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_default_qty = 10000000
    case_qty0 = 0
    case_qty1 = 2000000

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(details=base_rfq_details)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        check_qty(base_rfq_details, ar_service, case_id, case_default_qty)
        # Step 2
        modify_request.set_quantity(0)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty(base_rfq_details, ar_service, case_id, case_qty0)
        # Step 3
        modify_request.set_quantity(case_qty1)
        modify_request.set_change_currency()
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty(base_rfq_details, ar_service, case_id, case_qty1)
        # Step 4
        modify_request.set_quantity(0)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty(base_rfq_details, ar_service, case_id, case_qty0)
        #
        # modify_request.set_quantity(case_default_qty)
        # call(ar_service.modifyRFQTile, modify_request.build())
        # check_qty(base_rfq_details, ar_service, case_id, case_default_qty)
        #
        # modify_request.clear_quantity(True)
        # call(ar_service.modifyRFQTile, modify_request.build())
        # check_qty(base_rfq_details, ar_service, case_id, case_qty0)
        #
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
