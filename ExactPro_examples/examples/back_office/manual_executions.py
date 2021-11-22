from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ManualExecutingDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Manual executions example"

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
    else:
        get_opened_fe(case_id, session_id)

    try:
        service = Stubs.win_act_order_book

        manual_executing_details = ManualExecutingDetails(base_request)
        manual_executing_details.set_filter({"Order ID": "123456"})
        # manual_executing_details.set_row_number(1)

        executions_details = manual_executing_details.add_executions_details()
        executions_details.set_quantity("500")
        executions_details.set_price("400")
        executions_details.set_executing_firm("ExecutingFirm")
        executions_details.set_contra_firm("Contra_Firm")
        executions_details.set_last_capacity("Agency")

        call(service.manualExecution, manual_executing_details.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
