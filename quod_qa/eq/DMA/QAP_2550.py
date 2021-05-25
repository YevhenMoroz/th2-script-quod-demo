import logging
from datetime import datetime
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
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
    eq_wrappers.create_order(base_request, qty, client, 'XPAR', 'Limit', 'Day', True, 'CLIENTYMOROZ', '50', False,
                             True, False)
    # endregion

    # region verify value
    eq_wrappers.verify_value(base_request, case_id, 'Account ID', 'TestAccount')
    # endregion
    # create order with washbook
    eq_wrappers.create_order(base_request, qty, client, 'XPAR', 'Limit', 'Day', True, 'CLIENTYMOROZ', '50', True,
                             False, False)
    # region verify value
    eq_wrappers.verify_value(base_request, case_id, 'Wash Book', 'CareWB')
    # endregion
