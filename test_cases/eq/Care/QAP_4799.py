import logging
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import set_base
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4799"
    # region Declarations
    current_datetime = datetime.now()
    qty = "800"
    client = "CLIENT2"
    price = '40'
    instrument = {
        'Symbol': 'IS0000000001_EUR',
        'SecurityID': 'IS0000000001',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XEUR'
    }
    lookup = 'VATO'
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion
    # region Create order via FIX
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 1, price, instrument=instrument)
    # endregion
    eq_wrappers.accept_order(lookup, qty, price)
    eq_wrappers.split_order()
