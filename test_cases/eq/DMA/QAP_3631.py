import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import set_session_id, get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-3294"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT4"
    lookup = "PROL"
    last_mkt = 'DASI'
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion

    # region  Create order
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price)
    response = fix_message.pop('response')
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region notify DFD
    eq_wrappers.notify_dfd(base_request)
    # endregion

    # Check on ss
    params = {
        'OrderQty': qty,
        'ExecType': '3',
        'OrdStatus': '0',
        'Side': 1,
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }

    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
