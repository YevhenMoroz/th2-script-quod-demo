import logging

from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.utils import set_session_id, get_base_request

from quod_qa.wrapper import eq_wrappers


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "DMA_FixFE_test"
    case_id = create_event(case_name, report_id)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "100"
    price = "50"
    client = "CLIENT1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create DMA order
    try:
        eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
    except Exception:
        logger.error("Error execution", exc_info=True)

    # endregion

    # region Verify order
    eq_wrappers.verify_value(base_request, case_id, 'Sts', 'Open')
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
