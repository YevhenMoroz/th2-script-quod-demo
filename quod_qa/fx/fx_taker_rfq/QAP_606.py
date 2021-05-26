import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end, wk1_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile_swap(base_request, service, near_qty, cur1, cur2, near_tenor, far_tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_far_leg_tenor(far_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_dif(exec_id, base_request, service, case_id, near_date, far_date):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_swap_diff_days("ar_rfq.extract_swap_diff_days")
    dif = str(datetime.strptime(far_date, '%Y%m%d') - datetime.strptime(near_date, '%Y%m%d'))[:6]
    response = call(service.extractRFQTileValues, extract_value.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check swap diff")
    verifier.compare_values("Difference", dif, response["ar_rfq.extract_swap_diff_days"])
    verifier.verify()


def check_labels(exec_id, base_request, service, case_id, left_label, right_label):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_cur_label_left("ar_rfq.extract_label_left")
    extract_value.extract_cur_label_right("ar_rfq.extract_label_right")
    response = call(service.extractRFQTileValues, extract_value.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check labels")
    verifier.compare_values("Left label", left_label, response["ar_rfq.extract_label_left"])
    verifier.compare_values("Right label", right_label, response["ar_rfq.extract_label_right"])
    verifier.verify()


def check_tenor(exec_id, base_request, service, case_id, near_tenor, far_tenor):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_tenor("ar_rfq.extract_tenor")
    extract_value.extract_far_leg_tenor("ar_rfq.extract_far_leg_tenor")
    response = call(service.extractRFQTileValues, extract_value.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check tenors")
    verifier.compare_values("Near tenor", near_tenor, response["ar_rfq.extract_tenor"])
    verifier.compare_values("Far tenor", far_tenor, response["ar_rfq.extract_far_leg_tenor"])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_far_tenor = "1W"
    case_blank_tenor = ""
    case_near_date = spo_front_end()
    case_far_date = wk1_front_end()
    case_left_eur_label = "Sell EUR Far"
    case_right_eur_label = "Buy EUR Far"
    case_left_usd_label = "Buy USD Far"
    case_right_usd_label = "Sell USD Far"

    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "MMCLIENT2"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(base_rfq_details)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile_swap(base_rfq_details, ar_service, case_qty, case_from_currency,
                             case_to_currency, case_near_tenor, case_far_tenor, case_client)

        # Step 2
        check_dif("CD_0", base_rfq_details, ar_service, case_id, case_near_date, case_far_date)

        # Step 3
        modify_request.set_near_tenor(case_far_tenor)
        modify_request.set_far_leg_tenor(case_blank_tenor)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_tenor("CT_0", base_rfq_details, ar_service, case_id, case_far_tenor, case_blank_tenor)

        # Step 4
        modify_rfq_tile_swap(base_rfq_details, ar_service, case_qty, case_from_currency,
                             case_to_currency, case_near_tenor, case_far_tenor, case_client)
        check_labels("CL_0", base_rfq_details, ar_service, case_id, case_left_eur_label, case_right_eur_label)

        # Step 5
        modify_request.set_change_currency(True)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_labels("CL_1", base_rfq_details, ar_service, case_id, case_left_usd_label, case_right_usd_label)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
