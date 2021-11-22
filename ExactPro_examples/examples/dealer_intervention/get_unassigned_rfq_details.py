from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import ExtractionDetailsRequest, BaseTableDataRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Get UnAssigned RFQ details example"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
    username = Stubs.custom_config['qf_trading_fe_user_303']
    password = Stubs.custom_config['qf_trading_fe_password_303']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    try:
        service = Stubs.win_act_dealer_intervention_service

        base_data = BaseTableDataRequest(base=base_request)
        base_data.set_filter_dict({"Currency": "USD"})
        base_data.set_row_number(1)

        extraction_request = ExtractionDetailsRequest(base_data)
        extraction_request.set_extraction_id("ExtractionId")
        extraction_request.add_extraction_details([ExtractionDetail("dealerIntervention.venue", "Venue"),
                                                   ExtractionDetail("dealerIntervention.user", "User")])

        response = call(service.getUnassignedRFQDetails, extraction_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
