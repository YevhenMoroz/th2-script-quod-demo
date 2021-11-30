import logging

from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2550"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "800"
    client = "CLIENTSKYLPTOR"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region create order with account
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    eq_wrappers.create_order(base_request, qty, client, 'XPAR', 'Limit', 'Day', False, 'CLIENTYMOROZ', '50', False,
                             True, False)
    # endregion

    # region verify value
    eq_wrappers.verify_order_value(base_request, case_id, 'Account ID', 'TestAccount')
    # endregion
    # create order with wash_books
    eq_wrappers.create_order(base_request, qty, client, 'XPAR', 'Limit', 'Day', False, 'CLIENTYMOROZ', '50', True,
                             False, False)
    # region verify value
    eq_wrappers.verify_order_value(base_request, case_id, 'Wash Book', 'CareWB')
    # endregion
