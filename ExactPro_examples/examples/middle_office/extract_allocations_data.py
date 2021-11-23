from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import AllocationsExtractionDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Extract allocations details example"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    try:
        middle_office_service = Stubs.win_act_middle_office_service

        extract_request = AllocationsExtractionDetails(base=base_request)
        extract_request.set_block_filter({"Block ID": "123456"})
        extract_request.set_allocations_filter({"Alloc Qty": "0"})

        order_details = extract_request.add_order_details()
        order_details.set_order_number(1)
        order_details.add_extraction_detail(ExtractionDetail("middleOffice.status", "Status"))
        order_details.add_extraction_detail(ExtractionDetail("middleOffice.allocationId", "Allocation ID"))
        order_details.add_extraction_detail(ExtractionDetail("middleOffice.accountId", "Account ID"))

        response = call(middle_office_service.extractAllocationsTableData, extract_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
