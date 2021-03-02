from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import ModificationRequest
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Get RFQ details example"

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

        modify_request = ModificationRequest(base=base_request)
        modify_request.set_quote_ttl("123")
        modify_request.increase_ask()
        modify_request.decrease_ask()
        modify_request.increase_bid()
        modify_request.decrease_bid()
        modify_request.narrow_spread()
        modify_request.widen_spread()
        modify_request.skew_towards_ask()
        modify_request.skew_towards_bid()
        modify_request.send()
        # modification_request.reject()

        call(service.modifyAssignedRFQ, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
