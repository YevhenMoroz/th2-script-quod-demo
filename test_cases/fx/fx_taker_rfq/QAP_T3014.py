import logging
import time
from pathlib import Path
from th2_grpc_hand import rhbatch_pb2
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ExtractRFQTileValues, ModifyRFQTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile(base_request, service):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.click_checkbox_left()
    modify_request.click_checkbox_right()
    call(service.modifyRFQTile, modify_request.build())


def check_check_boxes(base_request, service, case_id, status):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_left_checkbox("ar_rfq.extract_left_checkbox")
    extract_value.extract_right_checkbox("ar_rfq.extract_right_checkbox")
    response = call(service.extractRFQTileValues, extract_value.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Checkboxes")
    verifier.compare_values("Left checkbox", status, response["ar_rfq.extract_left_checkbox"])
    verifier.compare_values("Right checkbox", status, response["ar_rfq.extract_right_checkbox"])
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    session_id_2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    session_id_3 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    case_base_request_2 = get_base_request(session_id_2, case_id)
    case_base_request_3 = get_base_request(session_id_3, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)
    base_rfq_details_2 = BaseTileDetails(base=case_base_request_2)
    base_rfq_details_3 = BaseTileDetails(base=case_base_request_3)

    case_sts_checked = "checked"
    case_sts_unchecked = "unchecked"

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        check_check_boxes(base_rfq_details, ar_service, case_id, case_sts_checked)
        # Step 2
        close_fe(case_id, session_id)
        time.sleep(5)
        # Step 3
        prepare_fe_2(case_id, session_id_2)
        create_or_get_rfq(base_rfq_details_2, ar_service)
        check_check_boxes(base_rfq_details_2, ar_service, case_id, case_sts_checked)
        # Step 4
        modify_rfq_tile(base_rfq_details_2, ar_service)
        check_check_boxes(base_rfq_details_2, ar_service, case_id, case_sts_unchecked)
        # Step 5
        close_fe(case_id, session_id_2)
        time.sleep(5)
        # Step 6
        prepare_fe_2(case_id, session_id_3)
        create_or_get_rfq(base_rfq_details_3, ar_service)
        check_check_boxes(base_rfq_details_3, ar_service, case_id, case_sts_unchecked)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details_3.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
