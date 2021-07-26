import logging
from datetime import datetime
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4627"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = "20"
    client = "DUMMY_CLIENT"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    eq_wrappers.isMenuItemPresent(base_request)
    # endregion

    # region Check value
    # eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Held")
    # eq_wrappers.verify_order_value(base_request, case_id, "Client Account Group ID", client)
    # region Execute
